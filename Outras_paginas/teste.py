import calendar
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Obter o ano e o mês atual
today = datetime.today()
year = st.number_input("Digite o ano:", int(today.year - 1), int(today.year + 1), today.year)
month = st.number_input("Digite o mês:", 1, 12, today.month)

# Criar o objeto de calendário para o mês e ano fornecidos
cal = calendar.monthcalendar(year, month)

# Mapear os números dos dias para letras
day_mapping = {0: "", 1: "A", 2: "B", 3: "C", 4: "D", 5: "E", 6: "F", 7: "G", 8: "H", 9: "I"}

# Criar uma lista de dicionários para armazenar os dados da escala
data = []

# Preencher a lista com as informações da escala
for week in cal:
    week_data = []
    for day in week:
        if day == 0:
            week_data.append("")
        else:
            # Mapear cada dígito do dia para a letra correspondente
            day_letters = "".join([day_mapping[int(digit)] for digit in str(day)])
            week_data.append(f"{day} / {day_letters}")
    data.append(week_data)

# Criar o DataFrame a partir da lista de listas
df = pd.DataFrame(data, columns=["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"])

# Exibir o DataFrame no Streamlit
st.table(df)

# Adicionar botão de download como imagem
fig, ax = plt.subplots(figsize=(8, 6))
ax.axis("off")  # Remover eixos
ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center', colColours=['#f3f3f3']*len(df.columns))
st.pyplot(fig)

# Adicionar botão de download
image_data = fig.canvas.tostring_rgb()
st.download_button(
    label="Baixar como Imagem",
    data=image_data,
    file_name=f"calendario_{year}_{month}.png",
    mime="image/png",
    key="download_button"
)
