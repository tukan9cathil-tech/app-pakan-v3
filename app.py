import streamlit as st

# Pengaturan Halaman Utama (Agar responsive di HP & Laptop)
st.set_page_config(
    page_title="AI Formulasi Pakan Ayam Pro",
    page_icon="🐔",
    layout="wide"
)

st.title("🐔 AI Formulasi Pakan Ayam & Solver Biaya Termurah")
st.write("Aplikasi cerdas multi-platform untuk mencari racikan pakan organik dengan biaya paling hemat secara otomatis dalam sekali klik.")

# ==========================================
# 1. DATABASE STANDAR NUTRISI TARGET AYAM
# ==========================================
TARGET_NUTRISI = {
    "Broiler Starter (0-3 Minggu)": {"protein": 22.0, "energi": 3000},
    "Broiler Finisher (>3 Minggu)": {"protein": 19.0, "energi": 3100},
    "Ayam Petelur / Layer (Produksi)": {"protein": 17.5, "energi": 2750}
}

# ==========================================
# 2. DATABASE BAHAN DASAR ORGANIK LOKAL
# ==========================================
BAHAN_BAKU = {
    "Jagung Kuning": {"cp": 8.5, "me": 3300, "harga_default": 6000, "ket": "Sumber Energi Utama"},
    "Bungkil Kedelai": {"cp": 44.0, "me": 2240, "harga_default": 11000, "ket": "Protein Nabati Tinggi"},
    "Dedak Padi / Bekatul": {"cp": 12.0, "me": 1600, "harga_default": 4000, "ket": "Serat & Karbohidrat"},
    "Tepung Ikan": {"cp": 55.0, "me": 2900, "harga_default": 14000, "ket": "Protein Hewani & Kalsium"},
    "Maggot BSF Kering": {"cp": 40.0, "me": 3750, "harga_default": 13000, "ket": "Protein Alternatif Super"},
    "Tepung Daun Kelor": {"cp": 27.0, "me": 2100, "harga_default": 8000, "ket": "Vitamin & Antioksidan"},
    "Azolla Microphylla Kering": {"cp": 24.0, "me": 1800, "harga_default": 5000, "ket": "Hijauan Protein Murah"},
    "Tepung Ampas Tahu": {"cp": 22.0, "me": 2400, "harga_default": 3500, "ket": "Limbah Organik Ekonomis"}
}

col1, col2 = st.columns()

# ==========================================
# PANEL KONTROL KIRI (INPUT USER & AI SOLVER)
# ==========================================
with col1:
    st.header("🛠️ Kontrol & Input Harga")
    
    # Pilih Jenis Ayam
    fase_ayam = st.selectbox("1. Pilih Jenis / Fase Ayam:", list(TARGET_NUTRISI.keys()))
    target = TARGET_NUTRISI[fase_ayam]
    
    st.info(f"📋 **Target Nutrisi Standar:**\n- Protein Kasar (CP): {target['protein']}%\n- Energi (ME): {target['energi']} kcal/kg")
    
    # Input Volume Produksi
    total_produksi = st.number_input("2. Total Pakan yang Dibuat (Kg):", min_value=1.0, value=100.0, step=10.0)
    
    st.write("---")
    st.subheader("3. Sesuaikan Harga Pasar Aktif (Rp / Kg)")
    
    # Dinamis input harga dari user
    harga_user = {}
    for nama_bahan, detail in BAHAN_BAKU.items():
        harga_user[nama_bahan] = st.number_input(f"Harga {nama_bahan}:", min_value=0, value=detail["harga_default"], step=500)

    st.write("---")
    st.subheader("⚡ Fitur One-Click AI Racikan")
    st.write("Klik tombol di bawah ini agar AI otomatis menghitung racikan dengan biaya termurah yang pas dengan target gizi.")
    
    tombol_ai = st.button("🤖 AI Optimasi: Cari Racikan Termurah", type="primary")

# ==========================================
# LOGIK SOLVER SELEKSI OTOMATIS (AI ALGORITHM)
# ==========================================
# Inisialisasi session state untuk menyimpan racikan slider
if "slider_vals" not in st.session_state:
    st.session_state.slider_vals = {nama: (25.0 if nama in ["Jagung Kuning", "Bungkil Kedelai", "Dedak Padi / Bekatul", "Tepung Ikan"] else 0.0) for nama in BAHAN_BAKU.keys()}

if tombol_ai:
    # Menggunakan metode pencarian heuristik sederhana untuk optimasi least-cost pakan
    best_cost = float('inf')
    best_recipe = None
    
    # Memilih kandidat kombinasi bahan organik secara cerdas berdasarkan bobot harga vs nutrisi
    # Untuk keandalan performa multi-platform tanpa library eksternal berat (seperti scipy), AI melakukan iterasi pencarian efisiensi tinggi
    for j_pct in range(30, 65, 5): # Jagung dominan energi
        for b_pct in range(10, 40, 5): # Bungkil dominan protein
            for d_pct in range(5, 30, 5): # Dedak penyeimbang biaya
                for m_pct in range(0, 25, 5): # Maggot sebagai booster protein alternatif
                    t_pct = 0 # Sisa bahan dihitung otomatis agar total pas 100%
                    ampas_pct = 100 - (j_pct + b_pct + d_pct + m_pct)
                    
                    if ampas_pct < 0 or ampas_pct > 30: 
                        continue
                        
                    # Hitung kandungan nutrisi dari kombinasi saat ini
                    cp_test = (j_pct*BAHAN_BAKU["Jagung Kuning"]["cp"] + 
                               b_pct*BAHAN_BAKU["Bungkil Kedelai"]["cp"] + 
                               d_pct*BAHAN_BAKU["Dedak Padi / Bekatul"]["cp"] + 
                               m_pct*BAHAN_BAKU["Maggot BSF Kering"]["cp"] + 
                               ampas_pct*BAHAN_BAKU["Tepung Ampas Tahu"]["cp"]) / 100.0
                               
                    me_test = (j_pct*BAHAN_BAKU["Jagung Kuning"]["me"] + 
                               b_pct*BAHAN_BAKU["Bungkil Kedelai"]["me"] + 
                               d_pct*BAHAN_BAKU["Dedak Padi / Bekatul"]["me"] + 
                               m_pct*BAHAN_BAKU["Maggot BSF Kering"]["me"] + 
                               ampas_pct*BAHAN_BAKU["Tepung Ampas Tahu"]["me"]) / 100.0
                    
                    # Cek kelayakan sesuai standar gizi ayam
                    if cp_test >= target["protein"] and me_test >= target["energi"]:
                        cost_test = (j_pct*harga_user["Jagung Kuning"] + 
                                     b_pct*harga_user["Bungkil Kedelai"] + 
                                     d_pct*harga_user["Dedak Padi / Bekatul"] + 
                                     m_pct*harga_user["Maggot BSF Kering"] + 
                                     ampas_pct*harga_user["Tepung Ampas Tahu"]) / 100.0
                        
                        if cost_test < best_cost:
                            best_cost = cost_test
                            best_recipe = {
                                "Jagung Kuning": float(j_pct),
                                "Bungkil Kedelai": float(b_pct),
                                "Dedak Padi / Bekatul": float(d_pct),
                                "Tepung Ikan": 0.0,
                                "Maggot BSF Kering": float(m_pct),
                                "Tepung Daun Kelor": 0.0,
                                "Azolla Microphylla Kering": 0.0,
                                "Tepung Ampas Tahu": float(ampas_pct)
                            }
                            
    if best_recipe:
        for nama in BAHAN_BAKU.keys():
            st.session_state.slider_vals[nama] = best_recipe.get(nama, 0.0)
        st.success("🤖 AI Sukses Menemukan Kombinasi Termurah & Paling Bergizi!")
    else:
        st.warning("⚠️ AI kesulitan mencari harga termurah dengan bahan saat ini. Coba turunkan harga atau gunakan bahan hewani tinggi protein.")

# ==========================================
# PANEL KONTROL KANAN (SLIDER RACIKAN & HASIL)
# ==========================================
with col2:
    st.header("⚖️ Komposisi Tambah/Kurang Manual")
    st.write("Persentase di bawah ini akan terisi otomatis saat Anda menekan tombol AI di sebelah kiri.")
    
    persentase = {}
    total_persen = 0
    
    for nama_bahan, detail in BAHAN_BAKU.items():
        persentase[nama_bahan] = st.slider(
            f"{nama_bahan} ({detail['ket']})", 
            min_value=0.0, 
            max_value=100.0, 
            value=st.session_state.slider_vals[nama_bahan], 
            step=0.5,
            key=f"slider_{nama_bahan}"
        )
        total_persen += persentase[nama_bahan]
    
    # Indikator validasi total persentase
    if total_persen == 100.0:
        st.success(f"⚖️ Total Komposisi: **{total_persen}%** (Pas!)")
    else:
        st.error(f"⚠️ Total Komposisi: **{total_persen}%**. Harus pas 100%! (Selisih: {100.0 - total_persen:.1f}%)")
        
    st.write("---")
    st.header("📊 Analisis Biaya & Nutrisi Hasil Akhir")
    
    # Perhitungan Nutrisi & Biaya Real-time
    total_protein = 0.0
    total_energi = 0.0
    total_biaya_per_kg = 0.0
    
    rincian_berat = {}
    rincian_biaya = {}
    
    for nama_bahan, pkn in persentase.items():
        porsi = pkn / 100.0
        total_protein += porsi * BAHAN_BAKU[nama_bahan]["cp"]
        total_energi += porsi * BAHAN_BAKU[nama_bahan]["me"]
        total_biaya_per_kg += porsi * harga_user[nama_bahan]
        
        rincian_berat[nama_bahan] = porsi * total_produksi
        rincian_biaya[nama_bahan] = rincian_berat[nama_bahan] * harga_user[nama_bahan]
        
    total_biaya_produksi = total_biaya_per_kg * total_produksi
    
    status_cp = "✅ Terpenuhi" if total_protein >= target["protein"] else "❌ Kurang"
    status_me = "✅ Terpenuhi" if total_energi >= target["energi"] else "❌ Kurang"
    
    c_nut1, c_nut2 = st.columns(2)
    with c_nut1:
        st.metric(label="Protein Kasar (CP) Terhitung", value=f"{total_protein:.2f} %", delta=f"{total_protein - target['protein']:.2f}% vs Target")
        st.write(f"Status Protein: **{status_cp}**")
    with c_nut2:
        st.metric(label="Energi Metabolis (ME) Terhitung", value=f"{int(total_energi)} kcal", delta=f"{int(total_energi - target['energi'])} kcal vs Target")
        st.write(f"Status Energi: **{status_me}**")
        
    st.write("---")
    st.subheader("💰 Ringkasan Kebutuhan Biaya")
    
    c_by1, c_by2 = st.columns(2)
    with c_by1:
        st.metric(label="Harga Pakan / Kg", value=f"Rp {int(total_biaya_per_kg):,}")
    with c_by2:
        st.metric(label="Total Biaya Produksi", value=f"Rp {int(total_biaya_produksi):,}", delta=f"Untuk {total_produksi} Kg")

    # Tabel Rincian Belanja Bahan Mentah
    st.write("---")
    st.subheader("📋 Daftar Timbangan Bahan untuk Pengadukan (Mixer)")
    
    data_tabel = []
    for nama_bahan in BAHAN_BAKU.keys():
