import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import ReduceLROnPlateau
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import KFold
from sklearn.metrics import roc_auc_score, f1_score
import numpy as np
from . import db
from .models import Intern, Progress
import os
import logging

class Attention(nn.Module):
    def __init__(self, hidden_size):
        super().__init__()
        self.attn = nn.Linear(hidden_size, 1)

    def forward(self, lstm_out):
        attn_weights = torch.softmax(self.attn(lstm_out), dim=1)
        return torch.sum(lstm_out * attn_weights, dim=1)

class AdvancedRiskLSTM(nn.Module):
    def __init__(self, input_size=10, hidden_size=64, num_layers=3):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, bidirectional=True)
        self.attention = Attention(hidden_size * 2)
        self.fc1 = nn.Linear(hidden_size * 2, 32)
        self.fc2 = nn.Linear(32, 1)
        self.dropout = nn.Dropout(0.4)

    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        attn_out = self.attention(lstm_out)
        out = self.dropout(torch.relu(self.fc1(attn_out)))
        return torch.sigmoid(self.fc2(out))

model = AdvancedRiskLSTM()
model_path = 'risk_model.pth'
if os.path.exists(model_path):
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
model.eval()

scaler = StandardScaler()
encoder_gender = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
encoder_drug = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
RISK_THRESHOLD = 0.5

def prepare_data():
    interns = Intern.query.all()
    data = []
    labels = []
    for intern in interns:
        progress = Progress.query.filter_by(intern_id=intern.id).order_by(Progress.week).all()
        if not progress:
            continue
        seq = []
        for p in progress:
            gender_enc = encoder_gender.fit_transform([[intern.gender]])[0]
            drug_enc = encoder_drug.fit_transform([[intern.initial_drug]])[0]
            features = [intern.age, p.wellbeing_score or 0, p.week, *gender_enc, *drug_enc]
            seq.append(features)
        data.append(np.array(seq))
        avg_score = np.mean([p.wellbeing_score for p in progress if p.wellbeing_score])
        labels.append(1 if avg_score < 50 else 0)
    if not data:
        # Synthetic data if no real data
        data = []
        labels = []
        for _ in range(200):
            seq_len = np.random.randint(4, 25)
            age = np.repeat(np.random.randint(18, 65), seq_len)
            gender = np.repeat(np.random.choice(['M', 'F', 'O']), seq_len)
            drug = np.repeat(np.random.choice(['Alcohol', 'Cocaine', 'Heroin', 'Other']), seq_len)
            weeks = np.arange(1, seq_len + 1)
            scores = np.clip(np.random.normal(60, 15, seq_len) + np.cumsum(np.random.normal(0, 3, seq_len)), 0, 100)
            gender_enc = encoder_gender.fit_transform(gender.reshape(-1, 1))
            drug_enc = encoder_drug.fit_transform(drug.reshape(-1, 1))
            seq = np.column_stack((age, scores, weeks, gender_enc, drug_enc))
            data.append(seq)
            labels.append(1 if np.mean(scores) < 50 else 0)
    max_len = max(len(seq) for seq in data)
    padded_data = [np.pad(seq, ((0, max_len - len(seq)), (0, 0)), 'constant') for seq in data]
    return np.array(padded_data), np.array(labels)

def train_model():
    try:
        data, labels = prepare_data()
        if len(data) < 10:
            logging.info("Datos insuficientes; skipping entrenamiento.")
            return
        data = scaler.fit_transform(data.reshape(-1, data.shape[-1])).reshape(data.shape)
        data = torch.tensor(data, dtype=torch.float32)
        labels = torch.tensor(labels, dtype=torch.float32).unsqueeze(1)

        kf = KFold(n_splits=5, shuffle=True, random_state=42)
        optimizer = optim.AdamW(model.parameters(), lr=0.0005, weight_decay=1e-4)
        criterion = nn.BCELoss()
        scheduler_lr = ReduceLROnPlateau(optimizer, 'min', patience=3, factor=0.5)
        best_loss = float('inf')
        for fold, (train_idx, val_idx) in enumerate(kf.split(data)):
            train_data, val_data = data[train_idx], data[val_idx]
            train_labels, val_labels = labels[train_idx], labels[val_idx]
            for epoch in range(150):
                model.train()
                optimizer.zero_grad()
                outputs = model(train_data)
                loss = criterion(outputs, train_labels)
                loss.backward()
                optimizer.step()
                if epoch % 10 == 0:
                    model.eval()
                    with torch.no_grad():
                        val_outputs = model(val_data)
                        val_loss = criterion(val_outputs, val_labels)
                    scheduler_lr.step(val_loss)
                    if val_loss < best_loss:
                        best_loss = val_loss
                        torch.save(model.state_dict(), model_path)
        # Final evaluation
        model.eval()
        with torch.no_grad():
            preds = model(data).numpy().flatten()
        auc = roc_auc_score(labels, preds)
        f1 = f1_score(labels, preds > RISK_THRESHOLD)
        app.logger.info(f"Modelo entrenado: AUC={auc:.2f}, F1={f1:.2f}")
    except Exception as e:
        app.logger.error(f'Error en train_model: {str(e)}')

def predict_risk(intern_id):
    intern = Intern.query.get(intern_id)
    progress = Progress.query.filter_by(intern_id=intern_id).order_by(Progress.week).all()
    if not progress:
        return 0.0
    seq = []
    for p in progress:
        gender_enc = encoder_gender.transform([[intern.gender]])[0]
        drug_enc = encoder_drug.transform([[intern.initial_drug]])[0]
        features = [intern.age, p.wellbeing_score or 0, p.week, *gender_enc, *drug_enc]
        seq.append(features)
    seq = np.array(seq)
    seq = scaler.transform(seq)
    seq = torch.tensor(seq.unsqueeze(0), dtype=torch.float32)
    model.eval()
    with torch.no_grad():
        risk = model(seq).item()
    return risk
