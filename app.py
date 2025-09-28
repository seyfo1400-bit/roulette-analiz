import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="Roulette Analiz", layout="wide")

st.title("🎲 Roulette Analiz ve Tahmin")

# Kullanıcıdan sayı listesi alma
numbers_input = st.text_area("Sayıları gir (virgülle ayır veya alt alta yaz):")

if numbers_input:
    # Sayıları temizle
    numbers = [int(x) for x in numbers_input.replace("\n", ",").split(",") if x.strip().isdigit()]
    df = pd.DataFrame(numbers, columns=["Sayı"])

    st.subheader("📌 Son Girilen Sayılar")
    st.write(df.tail(20))

    # Renk tablosu
    red_numbers = {1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36}
    black_numbers = {2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35}

    def get_color(n):
        if n == 0: return "🟢 Yeşil"
        elif n in red_numbers: return "🔴 Kırmızı"
        elif n in black_numbers: return "⚫ Siyah"
        else: return "❓"

    df["Renk"] = df["Sayı"].apply(get_color)

    # İstatistikler
    red_count = df["Renk"].value_counts().get("🔴 Kırmızı", 0)
    black_count = df["Renk"].value_counts().get("⚫ Siyah", 0)
    green_count = df["Renk"].value_counts().get("🟢 Yeşil", 0)

    st.subheader("📊 Genel İstatistikler")
    st.write(f"🔴 Kırmızı: {red_count} defa")
    st.write(f"⚫ Siyah: {black_count} defa")
    st.write(f"🟢 Yeşil: {green_count} defa")

    # En çok gelen sayılar
    top_numbers = df["Sayı"].value_counts().head(3).index.tolist()

    st.subheader("🎯 En Yüksek Olasılıklı 3 Sayı")
    st.write(", ".join(map(str, top_numbers)))

    # Belirli sayının ardından gelenler
    selected_number = st.number_input("Bir sayı seç (hangi sayının ardından ne gelmiş görmek için):", 0, 36, 0)

    following = []
    for i in range(len(numbers)-1):
        if numbers[i] == selected_number:
            following.append(numbers[i+1])

    if following:
        st.subheader(f"🔎 {selected_number} sayısından sonra gelenler")
        follow_df = pd.Series(following).value_counts()
        st.bar_chart(follow_df)
    else:
        st.info("Bu sayı hiç gelmemiş veya ardından başka sayı yok.")
else:
    st.info("Lütfen en az 1 sayı gir.")
