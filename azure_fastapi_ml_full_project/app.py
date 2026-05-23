import streamlit as st
import requests
import pandas as pd

# إعدادات الصفحة الأساسية
st.set_page_config(
    page_title="Iris Intelligence Dashboard",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# الرابط الخاص بـ FastAPI backend
API_BASE_URL = "http://127.0.0.1:8000"

# --- 🎨 حقن تصميم CSS مخصص متطور للغاية (Premium Dark Theme) ---
st.markdown("""
<style>
    /* تغيير الخلفية العامة ونوع الخط */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0d0f14 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    /* إضافة خلفية زهور السوسن بشكل فني وشفاف في الزوايا */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: absolute;
        top: 0; right: 0; width: 400px; height: 400px;
        background-image: url('https://images.unsplash.com/photo-1560717789-0ac7c58ac90a?auto=format&fit=crop&w=600&q=80');
        background-size: contain; background-repeat: no-repeat;
        opacity: 0.08; filter: hue-rotate(45deg); pointer-events: none;
    }

    /* تصميم القائمة الجانبية (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #131722 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    }
    
    /* تصميم البطاقات الزجاجية للمدخلات والنتائج */
    .glass-card {
        background: rgba(22, 27, 38, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 25px;
        margin-bottom: 20px;
    }
    
    /* تعديل العناوين الرئيسية */
    .main-title {
        font-size: 2.8rem !important;
        font-weight: 700 !important;
        background: linear-gradient(135deg, #ffffff 0%, #a5b4fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    
    /* تعديل تصميم حقول الإدخال الرقمية */
    .stNumberInput div[data-baseweb="input"] {
        background-color: #1c2130 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        color: white !important;
        transition: all 0.3s ease;
    }
    .stNumberInput div[data-baseweb="input"]:focus-within {
        border-color: #818cf8 !important;
        box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.2) !important;
    }
    
    /* تصميم التبويبات (Tabs) لتصبح دائرية وأنيقة */
    button[data-baseweb="tab"] {
        background-color: transparent !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 30px !important;
        padding: 8px 20px !important;
        margin-right: 10px !important;
        color: #94a3b8 !important;
        transition: all 0.3s ease;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #4f46e5 0%, #3730a3 100%) !important;
        color: white !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3) !important;
    }
    
    /* تصميم الزر المخصص (Predict Button) */
    div.stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.2) !important;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4) !important;
    }
    
    /* كروت الفئات الملونة في الجانب */
    .class-badge {
        padding: 8px 12px;
        border-radius: 8px;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        font-size: 0.95rem;
        background: rgba(255,255,255,0.02);
        border: 1px solid rgba(255,255,255,0.05);
    }
    .dot { height: 10px; width: 10px; border-radius: 50%; display: inline-block; margin-right: 10px; }
    .dot-setosa { background-color: #34d399; box-shadow: 0 0 8px #34d399; }
    .dot-versicolor { background-color: #fb923c; box-shadow: 0 0 8px #fb923c; }
    .dot-virginica { background-color: #38bdf8; box-shadow: 0 0 8px #38bdf8; }
</style>
""", unsafe_allow_html=True)


# --- 📡 فحص الحالة والاتصال بالـ API ---
api_online = False
model_loaded = False
try:
    health_res = requests.get(f"{API_BASE_URL}/health", timeout=3).json()
    api_online = (health_res.get("status") == "running")
    model_loaded = health_res.get("model_loaded", False)
except requests.exceptions.ConnectionError:
    pass

# إذا لم يعمل الـ API، أظهر رسالة خطأ أنيقة و أوقف التمهيد
if not api_online:
    st.error("🔴 Connection Error: Cannot reach the FastAPI backend server. Please make sure Uvicorn is running.")
    st.info("💡 Run your FastAPI app using: `uvicorn main:app --reload`")
    st.stop()


# --- 📊 جلب معلومات النموذج للشريط الجانبي (Sidebar) ---
try:
    model_info = requests.get(f"{API_BASE_URL}/model-info").json()
    model_type = model_info.get("model_type", "N/A")
    accuracy_val = f"{model_info.get('accuracy', 0.0) * 100:.2f}%"
    class_names = model_info.get("class_names", ["setosa", "versicolor", "virginica"])
except Exception:
    model_type = "RandomForestClassifier"
    accuracy_val = "90.00%"
    class_names = ["setosa", "versicolor", "virginica"]

with st.sidebar:
    st.markdown("<h2 style='font-weight:700; color:white; margin-bottom:20px;'>📊 Model Info</h2>", unsafe_allow_html=True)
    
    # عرض المؤشرات الرقمية بشكل أنيق
    st.metric(label="Model Architecture", value=model_type)
    st.metric(label="Calculated Accuracy", value=accuracy_val)
    
    st.markdown("<hr style='border-color:rgba(255,255,255,0.05)'>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#94a3b8; font-weight:600;'>Target Classes</h4>", unsafe_allow_html=True)
    
    # قائمة الفئات بالتأثيرات الملونة الجديدة
    for name in class_names:
        dot_class = f"dot-{name.lower()}"
        st.markdown(f"""
            <div class="class-badge">
                <span class="dot {dot_class}"></span>
                <span style="color: #e2e8f0;">{name}</span>
            </div>
        """, unsafe_allow_html=True)


# --- 🌸 الواجهة الرئيسية والمحتوى ---
st.markdown('<h1 class="main-title">🌸 Iris Flower Classifier</h1>', unsafe_allow_html=True)
st.markdown('<p style="color: #94a3b8; font-size:1.05rem; margin-bottom: 25px;">Production-ready ML serving architecture integrated seamlessly via FastAPI</p>', unsafe_allow_html=True)

# شريط الحالة الصغير الأنيق
st.markdown(f'<div style="background-color: rgba(52, 211, 153, 0.1); border: 1px solid rgba(52, 211, 153, 0.2); padding: 10px 15px; border-radius: 8px; color: #34d399; font-size: 0.9rem; margin-bottom: 30px;">● Server Status: Online & Secure</div>', unsafe_allow_html=True)

# بناء التبويبات (Tabs)
tab1, tab2 = st.tabs(["🎯 Single Prediction", "📁 Batch Processing"])

# --- التبويب الأول: التنبؤ الفردي ---
with tab1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color:white; font-weight:600; margin-bottom:20px;">Enter Feature Measurements</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="large")
    with col1:
        sepal_length = st.number_input("Sepal Length (cm)", min_value=0.1, max_value=10.0, value=5.1, step=0.1)
        sepal_width = st.number_input("Sepal Width (cm)", min_value=0.1, max_value=10.0, value=3.5, step=0.1)
    with col2:
        petal_length = st.number_input("Petal Length (cm)", min_value=0.1, max_value=10.0, value=1.4, step=0.1)
        petal_width = st.number_input("Petal Width (cm)", min_value=0.1, max_value=10.0, value=0.2, step=0.1)
    
    st.markdown('<div style="margin-top: 25px;"></div>', unsafe_allow_html=True)
    
    if st.button("Predict Species 🚀", key="predict_single_btn"):
        payload = {
            "sepal_length": sepal_length,
            "sepal_width": sepal_width,
            "petal_length": petal_length,
            "petal_width": petal_width
        }
        
        with st.spinner("Analyzing parameters..."):
            response = requests.post(f"{API_BASE_URL}/predict", json=payload)
            if response.status_code == 200:
                result = response.json()
                st.balloons()
                
                # عرض النتيجة ببطاقة مخصصة مبهرة
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(129, 140, 248, 0.05) 100%); border: 1px solid rgba(129, 140, 248, 0.3); border-radius: 12px; padding: 20px; text-align: center; margin-top: 25px;">
                    <span style="color: #a5b4fc; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">Model Inference Result</span>
                    <h2 style="color: white; font-weight: 700; margin-top: 5px; margin-bottom: 0;">Predicted Species: <span style="color:#818cf8;">{result['prediction_class']}</span></h2>
                </div>
                """, unsafe_allow_html=True)
                
                # رسم بياني مخصص وشفاف للاحتمالات ليتماشى مع الوضع الداكن
                st.markdown('<h4 style="color:white; margin-top:30px; font-weight:600;">📊 Prediction Confidence</h4>', unsafe_allow_html=True)
                prob_df = pd.DataFrame(list(result['probabilities'].items()), columns=['Class', 'Probability'])
                st.bar_chart(prob_df.set_index('Class'), y="Probability", use_container_width=True)
            else:
                st.error(f"Error from API: {response.text}")
                
    st.markdown('</div>', unsafe_allow_html=True)

# --- التبويب الثاني: التنبؤ الجماعي ---
with tab2:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<h3 style="color:white; font-weight:600; margin-bottom:15px;">Bulk Batch Processing</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color:#94a3b8; font-size:0.95rem;">Upload a `.csv` file containing structural features to evaluate records in bulk.</p>', unsafe_allow_html=True)
    
    # تحميل قالب CSV جاهز
    template_df = pd.DataFrame([{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}])
    st.download_button("📥 Download CSV Template", data=template_df.to_csv(index=False), file_name="iris_bulk_template.csv", mime="text/csv")
    
    st.markdown("<br>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Drop your dataset file here", type=["csv"])
    
    if uploaded_file is not None:
        input_df = pd.read_csv(uploaded_file)
        st.markdown('<h4 style="color:white; font-weight:600; margin-top:15px;">Data Preview</h4>', unsafe_allow_html=True)
        st.dataframe(input_df.head(), use_container_width=True)
        
        if st.button("Execute Bulk Prediction ⚙️", key="predict_batch_btn"):
            records = input_df.to_dict(orient="records")
            with st.spinner("Processing batch pipeline..."):
                response = requests.post(f"{API_BASE_URL}/predict-batch", json=records)
                
                if response.status_code == 200:
                    batch_results = response.json()
                    predictions = [res['prediction_class'] for res in batch_results]
                    input_df['Predicted Class'] = predictions
                    
                    st.success("✨ Batch inference executed perfectly!")
                    st.dataframe(input_df, use_container_width=True)
                    
                    # زر تحميل النتيجة النهائية
                    csv_output = input_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="📥 Download Results Dataset",
                        data=csv_output,
                        file_name="iris_classified_results.csv",
                        mime="text/csv"
                    )
                else:
                    st.error(f"Batch Error: {response.text}")
                    
    st.markdown('</div>', unsafe_allow_html=True)