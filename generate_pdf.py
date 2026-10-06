import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#1B365D"))
        
        if self._pageNumber > 1:
            self.drawString(54, 11 * inch - 36, "WILDFIRE PREDICTION & EARLY DETECTION: A COMPARATIVE REVIEW")
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#666666"))
            self.drawRightString(8.5 * inch - 54, 11 * inch - 36, "RESEARCH REVIEW ARTICLE")
            self.setStrokeColor(colors.HexColor("#D0D7DE"))
            self.setLineWidth(0.75)
            self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)
            
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 36, page_str)
        self.drawString(54, 36, "COMPARATIVE RESEARCH SYNTHESIS")
        self.setStrokeColor(colors.HexColor("#D0D7DE"))
        self.setLineWidth(0.75)
        self.line(54, 48, 8.5 * inch - 54, 48)
        self.restoreState()

def build_pdf(filename="Machine_Learning_Wildfire_Comparative_Review.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    PRIMARY = colors.HexColor("#1B365D")
    SECONDARY = colors.HexColor("#0B66C2")
    DARK_TEXT = colors.HexColor("#222222")
    MUTED_TEXT = colors.HexColor("#555555")
    BG_LIGHT = colors.HexColor("#F8F9FA")
    BORDER_COLOR = colors.HexColor("#D0D7DE")
    
    title_style = ParagraphStyle('DocTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=20, leading=25, textColor=PRIMARY, spaceAfter=12)
    meta_style = ParagraphStyle('DocMeta', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=10, leading=14, textColor=MUTED_TEXT, spaceAfter=15)
    abstract_body = ParagraphStyle('AbstractBody', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5, leading=14, textColor=DARK_TEXT, spaceAfter=10)
    h1_style = ParagraphStyle('Heading1_Custom', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=13, leading=17, textColor=PRIMARY, spaceBefore=14, spaceAfter=6, keepWithNext=True)
    h2_style = ParagraphStyle('Heading2_Custom', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=11, leading=15, textColor=SECONDARY, spaceBefore=10, spaceAfter=4, keepWithNext=True)
    body_style = ParagraphStyle('Body_Custom', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5, leading=14.5, textColor=DARK_TEXT, spaceAfter=8, alignment=4)
    bullet_style = ParagraphStyle('Bullet_Custom', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5, leading=14, textColor=DARK_TEXT, leftIndent=15, firstLineIndent=-10, spaceAfter=4)
    table_hdr_style = ParagraphStyle('TableHdr', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8.5, leading=11, textColor=colors.white, alignment=1)
    table_cell_bold = ParagraphStyle('TableCellBold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=11, textColor=PRIMARY)
    table_cell_text = ParagraphStyle('TableCellText', parent=styles['Normal'], fontName='Helvetica', fontSize=7.5, leading=10.5, textColor=DARK_TEXT)

    story = []
    
    story.append(Paragraph("Machine Learning, Remote Sensing, and GIS for Wildfire Prediction and Early Detection: A Comparative Review of Methods, Accuracy, Tools, and Limitations", title_style))
    story.append(Paragraph("<b>Comparative Research Review</b> &nbsp;|&nbsp; <i>Methodological Analysis of Predictive Models</i>", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=0, spaceAfter=12))
    
    abstract_text = (
        "<b>Abstract—</b>Wildfires present major environmental, social, and economic hazards, creating a need for effective systems that predict fire occurrence, map spatial risk zones, and identify smoke at early stages. Advances in machine learning (ML), deep learning, geographic information systems (GIS), remote sensing, and video surveillance have expanded the ability of fire management agencies to analyze multi-source spatial-temporal datasets. This review compares seven published studies applying ML, GIS, satellite imagery, weather records, and computer vision to wildfire management. The evaluated architectures include U-Net–long short-term memory (ULSTM) networks, Random Forest regression and classification, artificial neural networks (ANN), support vector machines (SVM), spatial deep neural networks (DNN) combined with multi-criteria decision analysis (MCDA), GIS weighted overlay, and attention-enhanced bidirectional LSTM (ABi-LSTM) models. Results show that multimodal and spatial-temporal approaches consistently achieve strong predictive performance, with reported accuracies ranging from 75.8% to 97.8%. Random Forest models performed well on structured tabular and spatial data, while deep learning models performed best on high-dimensional video and multi-spectral imagery. However, current research exhibits limitations, including narrow geographic scope, lack of real-time data integration, data scarcity, inconsistent evaluation metrics, and the exclusion of key physical factors such as fine fuel load and soil moisture. Future systems should emphasize real-time data fusion, multi-regional validation, and interpretable model design to better support operational decision-making."
    )
    
    abstract_table = Table([[Paragraph(abstract_text, abstract_body)]], colWidths=[7.0*inch])
    abstract_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(abstract_table)
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Keywords:</b> wildfire prediction; machine learning; remote sensing; GIS; Random Forest; deep learning; smoke detection; spatial-temporal modeling; early warning systems.", body_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=0.5, color=BORDER_COLOR, spaceBefore=4, spaceAfter=12))
    
    story.append(Paragraph("1. Introduction", h1_style))
    story.append(Paragraph("Wildfires cause severe damage to forest ecosystems, agricultural land, infrastructure, and human settlements. Wildfire activity depends on complex interactions among weather conditions, vegetation characteristics, topography, human land use, and ignition sources such as lightning. In recent years, higher temperatures, extended droughts, and expanding wildland-urban interfaces have increased fire frequency and intensity across diverse geographic regions.", body_style))
    story.append(Paragraph("Traditional wildfire management relies on manual observation posts, historical fire logs, and weather indices such as the Canadian Forest Fire Weather Index (FWI) or the National Fire Danger Rating System (NFDRS). While these traditional frameworks provide basic operational guidelines, they struggle to capture non-linear interactions among changing environmental and human factors. Machine learning (ML) and deep learning (DL) provide alternative methods by learning patterns directly from complex, multi-source datasets.", body_style))
    story.append(Paragraph("Recent studies examine various data sources, including satellite imagery, Digital Elevation Models (DEM), historical ignition points, air quality measurements, local weather station feeds, and video streams. Analytical methods range from decision tree ensembles (such as Random Forest) to neural network architectures, including Convolutional Neural Networks (CNN), Long Short-Term Memory (LSTM) networks, and GIS multi-criteria evaluation models.", body_style))
    story.append(Paragraph("This paper presents a comparative review of seven representative studies focused on wildfire prediction, risk zoning, and early smoke recognition. By analyzing model structures, data inputs, software tools, performance metrics, and key limitations, this review summarizes current progress in wildfire modeling and highlights practical directions for future system design.", body_style))
    
    story.append(Paragraph("2. Research Objectives", h1_style))
    story.append(Paragraph("This comparative review addresses five specific objectives:", body_style))
    story.append(Paragraph("• <b>Evaluate Modeling Paradigms:</b> Analyze how machine learning, deep neural networks, remote sensing, GIS modeling, and computer vision are applied in wildfire management.", bullet_style))
    story.append(Paragraph("• <b>Compare Research Methodologies:</b> Examine datasets, feature selection methods, software tools, and model architectures across the selected studies.", bullet_style))
    story.append(Paragraph("• <b>Assess Model Performance:</b> Review reported metrics, including Accuracy, ROC-AUC, Precision, Recall, F1-Score, Kappa, and RMSE across different tasks.", bullet_style))
    story.append(Paragraph("• <b>Identify Core Limitations:</b> Identify common weaknesses, such as geographic constraints, absence of real-time data, missing fuel variables, and evaluation inconsistencies.", bullet_style))
    story.append(Paragraph("• <b>Provide Practical Recommendations:</b> Outline realistic technical steps to improve the reliability, scalability, and clarity of future early warning systems.", bullet_style))
    
    story.append(Paragraph("3. Literature Background", h1_style))
    story.append(Paragraph("Wildfire research typically focuses on three main operational tasks: (1) <i>fire occurrence prediction</i>, (2) <i>spatial fire risk mapping</i>, and (3) <i>early fire and smoke detection</i>. Occurrence prediction estimates the probability of fire ignition within specific spatial units over time. Spatial risk mapping combines terrain, vegetation, and exposure factors to categorize regional vulnerability. Early detection identifies active flames or smoke plumes using visual, thermal, or satellite sensors.", body_style))
    story.append(Paragraph("Machine learning methods are suited for wildfire modeling because fire occurrence involves multiple interacting variables. For example, dry vegetation and low humidity do not cause a fire without an ignition source, such as lightning or human activity. ML algorithms process these combined variables without requiring explicit mathematical formulas for physical fire behavior.", body_style))
    story.append(Paragraph("Ensemble algorithms, particularly Random Forest (RF), serve as common baselines in spatial fire modeling. RF handles tabular datasets, models non-linear relationships, resists overfitting, and ranks feature importance. Literature reviews (e.g., Alkhatib et al., 2023) confirm that RF and CNN models consistently produce strong results across various forest types. However, data scarcity, high computation demands, and inconsistent testing procedures remain widespread challenges.", body_style))
    story.append(Paragraph("Geographic Information Systems (GIS) and satellite remote sensing supply essential spatial data. Satellite platforms (such as Landsat, MODIS, and Sentinel) monitor vegetation status (NDVI), land cover, and surface temperature. GIS platforms combine these layers with terrain data (slope, aspect, elevation) and distance buffers around roads and settlements. Early work by Jaiswal et al. (2002) showed how combining spatial variables in GIS creates usable fire risk maps.", body_style))
    story.append(Paragraph("Deep learning models have expanded spatial-temporal analysis by processing complex sequential data. Hybrid models combining spatial feature extraction with temporal sequence processing—such as U-Net–LSTM architectures—capture terrain conditions alongside changing weather patterns. Similarly, computer vision models with temporal attention mechanisms (such as Attention-Enhanced Bi-LSTM) analyze video frames to identify moving smoke plumes before thermal signatures appear on satellite sensors.", body_style))

    story.append(Paragraph("4. Methodology", h1_style))
    story.append(Paragraph("4.1 Research Design", h2_style))
    story.append(Paragraph("This study uses a comparative review approach. Instead of gathering new field data, it systematically analyzes seven published studies representing different methods, study regions, and modeling objectives within wildfire research.", body_style))
    story.append(Paragraph("Each study was examined across seven standard categories:", body_style))
    story.append(Paragraph("• <b>Primary Objective:</b> The main target (occurrence prediction, risk mapping, or smoke detection).", bullet_style))
    story.append(Paragraph("• <b>Data Sources:</b> Input datasets (satellite imagery, weather records, DEM, video feeds, census data).", bullet_style))
    story.append(Paragraph("• <b>Methodological Design:</b> Data processing steps, sampling choices, and validation setups.", bullet_style))
    story.append(Paragraph("• <b>Analytical Models:</b> Main algorithms (Random Forest, CNN, LSTM, MLP, AHP, SVM).", bullet_style))
    story.append(Paragraph("• <b>Software & Tools:</b> Programs used (Python, PyTorch, TensorFlow, Google Earth Engine, ArcGIS).", bullet_style))
    story.append(Paragraph("• <b>Evaluation Metrics & Results:</b> Reported performance values (Accuracy, AUC, Kappa, RMSE).", bullet_style))
    story.append(Paragraph("• <b>Key Limitations:</b> Practical, geographical, or structural constraints.", bullet_style))

    story.append(Paragraph("4.2 Studies Included", h2_style))
    story.append(Paragraph("The seven benchmark studies selected for detailed evaluation include:", body_style))
    story.append(Paragraph("1. A multimodal spatial-temporal wildfire prediction system using a ULSTM framework (U-Net + LSTM).", bullet_style))
    story.append(Paragraph("2. A comprehensive review of machine learning algorithms across forest fire science applications (Alkhatib et al., 2023).", bullet_style))
    story.append(Paragraph("3. A GIS-based satellite remote sensing fire risk zoning study in tropical forests (Jaiswal et al., 2002).", bullet_style))
    story.append(Paragraph("4. A national-scale forest fire occurrence prediction study comparing four ML algorithms in China (Pang et al., 2022).", bullet_style))
    story.append(Paragraph("5. An ensemble Random Forest regression model predicting wildfire probability in Central India (Singh & Jeganathan, 2024).", bullet_style))
    story.append(Paragraph("6. A spatial deep neural network and multi-criteria decision framework for composite risk mapping in Sydney (Naderpour et al., 2021).", bullet_style))
    story.append(Paragraph("7. An attention-enhanced bidirectional LSTM computer vision network for early video smoke recognition (Cao et al., 2019).", bullet_style))

    story.append(Spacer(1, 8))
    story.append(Paragraph("<b>Table 1: Comparative Synthesis Matrix of Reviewed Wildfire Studies</b>", ParagraphStyle('TableCaption', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, textColor=PRIMARY, spaceAfter=6)))
    
    table_data = [
        [
            Paragraph("Paper Title & Study Focus", table_hdr_style),
            Paragraph("Objective", table_hdr_style),
            Paragraph("Data Used", table_hdr_style),
            Paragraph("Methodology & Technique", table_hdr_style),
            Paragraph("Tools & Software", table_hdr_style),
            Paragraph("Key Results & Performance", table_hdr_style),
            Paragraph("Core Limitations", table_hdr_style)
        ]
    ]
    
    papers_raw = [
        (
            "<b>1. Multimodal Wildfire Prediction System</b><br/>(2023)",
            "Develop a multimodal ML system for spatial-temporal wildfire prediction and early warning.",
            "Historical wildfire records, weather variables, environmental/air-quality metrics, geological layers.",
            "Spatial-temporal data processing + ULSTM network combining U-Net spatial modeling with LSTM temporal sequence learning.",
            "Python, PyTorch, Google Earth Engine (GEE).",
            "<b>Accuracy: 97.1%</b><br/>Outperformed standard CNN baselines across combined spatial-temporal inputs.",
            "Lower accuracy for small-scale fires and unpredictable human or lightning ignition events."
        ),
        (
            "<b>2. Machine Learning Review in Forest Fire Science</b><br/><i>Alkhatib et al. (2023)</i>",
            "Map ML applications in forest fire research to match algorithms with specific domain characteristics.",
            "Satellite imagery, UAV thermal feeds, weather datasets, public repositories.",
            "Systematic review evaluating Random Forest, CNNs, SVMs, and traditional empirical frameworks.",
            "Google Earth Engine, NASA TERRA/AQUA platforms, UAV imaging tools.",
            "Random Forest and CNN architectures consistently performed best across multiple domains.",
            "Data scarcity, high computational demands, unstandardized evaluation metrics, data quality issues."
        ),
        (
            "<b>3. GIS & Satellite Fire Risk Mapping</b><br/><i>Jaiswal et al. (2002)</i>",
            "Map forest fire risk zones by combining satellite imagery, terrain data, and settlement proximity.",
            "Landsat TM imagery (1992, 1998), topographical maps, DEM, forest type maps, weather data, road/settlement buffers.",
            "Supervised classification (Maximum Likelihood), slope/aspect analysis, distance buffering, weighted GIS index formula.",
            "ERDAS Imagine, ER Mapper, ArcGIS, MapInfo.",
            "Classification Accuracy: <b>93.75% (1992)</b> and <b>90.25% (1998)</b>. Derived 5 distinct risk zones.",
            "No independent validation of final risk map; cloud/fog cover affected 1992 forest change analysis."
        ),
        (
            "<b>4. ML Fire Occurrence in China</b><br/><i>Pang et al. (2022)</i>",
            "Predict national forest fire occurrence probability combining weather, geography, vegetation, and human activity.",
            "NASA Global Fire Atlas, China weather station network, DEM, geographic/socioeconomic layers (6 major sources).",
            "Comparative evaluation of 4 ML algorithms: Random Forest (RF), ANN, RBFNN, and Support Vector Machines (SVM).",
            "R, Python, GIS software.",
            "Accuracy range: 75.8%–89.2%, AUC: 0.840–0.960.<br/><b>RF best: 89.2% Acc, 0.960 AUC.</b>",
            "Omitted fine fuel load and combustible tree species; evaluated only four traditional ML models."
        ),
        (
            "<b>5. Random Forest Fire Probability in India</b><br/><i>Singh & Jeganathan (2024)</i>",
            "Examine spatial-temporal fire patterns (2001–2020) and model future fire probability in Central India.",
            "MODIS FIRMS active fire points, MODIS LST, MODIS NDVI, CHIRPS rainfall, ASTER DEM.",
            "Grid sampling, fishnet feature extraction, Random Forest Regression modeling with K-fold cross-validation.",
            "Python, Scikit-learn, Google Earth Engine, NASA MODIS/FIRMS.",
            "<b>ROC: 95.1%, PRC: 93.8%, Kappa: 94.3%, RMSE: 0.165.</b><br/>Road density was the strongest predictor.",
            "Excluded real-time soil moisture, fine fuel loads, combustible species distribution, and local biodiversity indicators."
        ),
        (
            "<b>6. Spatial DNN Composite Risk Mapping</b><br/><i>Naderpour et al. (2021)</i>",
            "Combine fire hazard susceptibility with socio-economic vulnerability to create a composite risk map for Sydney.",
            "12 environmental layers (1m resolution), 250 ignition points, 24 census vulnerability indicators, LiDAR, Spot-6.",
            "Multilayer Perceptron (MLP) for hazard susceptibility + Analytic Hierarchy Process (AHP) for vulnerability weighting.",
            "GIS raster overlay, FbSP hyperparameter optimization, AHP pairwise evaluation.",
            "<b>ROC: 95.1%, PRC: 93.8%, Kappa: 94.3%, RMSE: 0.165.</b><br/>Converted hazard maps into operational risk zones.",
            "Tested in a single region; static inputs; omitted fuel/moisture variables; AHP weights relied on expert judgment."
        ),
        (
            "<b>7. Attention-Enhanced Bi-LSTM Smoke Recognition</b><br/><i>Cao et al. (2019)</i>",
            "Detect forest fire smoke early from video feeds by modeling spatial features and dynamic motion patterns.",
            "Custom video dataset (2,000 sequences: 1,000 smoke, 1,000 non-smoke; 20 frames @ 5fps, 299x299 resolution).",
            "ViBe background subtraction + Inception V3 spatial feature extraction + Attention-Enhanced Bi-LSTM (ABi-LSTM).",
            "TensorFlow, ImageNet-pretrained Inception V3, RMSprop/Adam, NVIDIA GTX 1080 GPU.",
            "<b>Accuracy: 97.8% (TPR 97.5%, TNR 98.0%).</b><br/>+4.4% gain over single-frame baseline; 0.096s runtime per sequence.",
            "Used a non-public dataset (limiting independent testing); untested in night or fog conditions; whole sequence classification only."
        )
    ]
    
    col_widths = [1.1*inch, 1.0*inch, 1.0*inch, 1.1*inch, 0.8*inch, 1.0*inch, 1.0*inch]
    
    for row in papers_raw:
        table_data.append([
            Paragraph(row[0], table_cell_bold),
            Paragraph(row[1], table_cell_text),
            Paragraph(row[2], table_cell_text),
            Paragraph(row[3], table_cell_text),
            Paragraph(row[4], table_cell_text),
            Paragraph(row[5], table_cell_text),
            Paragraph(row[6], table_cell_text)
        ])
        
    comp_table = Table(table_data, colWidths=col_widths, repeatRows=1)
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ALIGN', (0,0), (-1,0), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT])
    ]))
    
    story.append(comp_table)
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("4.3 Comparative Evaluation Framework", h2_style))
    story.append(Paragraph("The comparative evaluation was structured around primary operational tasks. Fire occurrence models were evaluated on their ability to estimate fire probability across grid cells; risk mapping studies were assessed on their multi-layer GIS integration; and video detection models were evaluated on latency and motion recognition accuracy.", body_style))
    story.append(Paragraph("Evaluated performance metrics included raw Accuracy, Precision, Recall, F1-score, Receiver Operating Characteristic Area Under Curve (ROC-AUC), Precision-Recall Curve (PRC), Cohen's Kappa, Root Mean Square Error (RMSE), True Positive Rate (TPR), and True Negative Rate (TNR). Because individual studies used different datasets and sampling methods, reported values reflect relative model capability within specific test conditions rather than direct absolute equivalents.", body_style))

    story.append(Paragraph("5. Results and Comparative Analysis", h1_style))
    story.append(Paragraph("5.1 Multimodal Machine Learning for Wildfire Prediction", h2_style))
    story.append(Paragraph("The ULSTM model in Study 1 combined fire history records, weather data (temperature, humidity, rainfall, wind speed), air quality metrics, and terrain variables. Achieving a classification accuracy of 97.1%, the ULSTM network demonstrated that combining multiple data types improves prediction performance compared to single-source CNN baselines.", body_style))
    story.append(Paragraph("The primary design feature of ULSTM is its separate spatial and temporal processing: U-Net modules extract spatial patterns from terrain and vegetation layers, while bidirectional LSTM layers process changing weather trends over time. This combined modeling is useful because fire risk depends on both static land features and short-term weather changes. However, the model performed less accurately on small fires (< 1 hectare) and unexpected human-caused ignitions, showing the difficulty of predicting irregular events.", body_style))

    story.append(Paragraph("5.2 GIS and Satellite-Based Fire-Risk Mapping", h2_style))
    story.append(Paragraph("Jaiswal et al. (2002) evaluated spatial risk mapping using Landsat TM imagery (1992, 1998), elevation models, vegetation maps, and settlement distance buffers. Supervised maximum likelihood classification achieved land-cover accuracies of 93.75% for 1992 and 90.25% for 1998. The authors used a weighted index formula: $RC = 7(VT) + 5(S+A) + 3(DR+DS)$, where $VT$ represents vegetation type, $S+A$ terrain slope and aspect, and $DR+DS$ road and settlement proximity.", body_style))
    story.append(Paragraph("While the resulting five-category risk map provided clear visual information for planning, two weaknesses were present: first, cloud and fog interference in early satellite images reduced change detection accuracy; second, the study evaluated classification accuracy of input layers rather than testing the final risk map against independent ground fire data.", body_style))

    story.append(Paragraph("5.3 Machine-Learning Models for Fire Occurrence Prediction", h2_style))
    story.append(Paragraph("Pang et al. (2022) compared four algorithms across China using six data sources. Testing Random Forest, Artificial Neural Networks, Radial Basis Function Neural Networks, and Support Vector Machines, Random Forest achieved the highest performance (89.2% Accuracy, 0.960 ROC-AUC), compared to SVM (75.8% Accuracy). The decision tree ensemble handled complex interactions across varied geographical regions without significant overfitting.", body_style))
    story.append(Paragraph("However, the study did not include variables such as fine fuel accumulation, fuel moisture content, or tree species composition. In addition, limiting the evaluation to four algorithms left modern gradient-boosting models (such as XGBoost or LightGBM) and neural network variations unexamined.", body_style))

    story.append(Paragraph("5.4 Random Forest Prediction in India", h2_style))
    story.append(Paragraph("Singh & Jeganathan (2024) modeled fire probability across Madhya Pradesh and Chhattisgarh using 20 years (2001–2020) of NASA MODIS FIRMS fire data, Land Surface Temperature (LST), NDVI vegetation values, CHIRPS rainfall, and ASTER elevation layers. Random Forest Regression yielded stable performance: ROC-AUC = 95.1%, PRC = 93.8%, Kappa = 94.3%, and RMSE = 0.165.", body_style))
    story.append(Paragraph("Feature importance analysis indicated that road density and distance to settlements were the strongest predictors of fire activity. This result emphasizes the major role of human access in regional fire occurrence. However, the study relied on static environmental inputs and omitted dynamic soil moisture and fuel load indicators.", body_style))

    story.append(Paragraph("5.5 Deep Neural Networks and Composite Wildfire Risk", h2_style))
    story.append(Paragraph("Naderpour et al. (2021) developed a composite risk model for Sydney's Northern Beaches, separating physical hazard susceptibility from human vulnerability. A 3-hidden-layer Multilayer Perceptron (MLP) evaluated 12 environmental layers to estimate fire hazard (ROC-AUC = 95.1%), while an Analytic Hierarchy Process (AHP) weighted 24 census factors to evaluate population exposure.", body_style))
    story.append(Paragraph("The findings demonstrated that areas with high natural hazard (such as dense forests) did not automatically result in high total risk unless human infrastructure or settlements were nearby. However, using expert judgment for AHP weights introduces potential subjectivity, and relying on static census limits dynamic risk updating.", body_style))

    story.append(Paragraph("5.6 Video-Based Smoke Recognition", h2_style))
    story.append(Paragraph("Cao et al. (2019) focused on early visual detection using video feeds, proposing an Attention-Enhanced Bidirectional LSTM (ABi-LSTM) model. The system used ViBe background subtraction to locate candidate areas, Inception V3 to extract visual features, and a temporal-attention Bi-LSTM to analyze motion patterns across 20-frame sequences (5 fps).", body_style))
    story.append(Paragraph("ABi-LSTM achieved 97.8% accuracy (TPR 97.5%, TNR 98.0%), representing a 4.4% improvement over single-frame CNN models with an average processing time of 0.096 seconds per sequence. Ablation analysis showed that bidirectional temporal modeling added 2.1% accuracy and the attention mechanism added 2.3%. Main constraints included testing on a private dataset, lack of night or fog evaluations, and outputting sequence-level classifications rather than localized bounding boxes.", body_style))

    story.append(Paragraph("6. Discussion", h1_style))
    story.append(Paragraph("Comparing results across all seven studies indicates that multimodal models and spatial-temporal architectures generally perform better than single-source or static models. The highest accuracies—97.8% in video smoke recognition (Cao et al., 2019) and 97.1% in multimodal risk prediction—were achieved by hybrid deep learning models that process both spatial structure and temporal changes.", body_style))
    story.append(Paragraph("Random Forest remains an effective algorithm for structured tabular and spatial data, offering consistent performance, low sensitivity to hyperparameter choices, and direct feature importance output (Pang et al., 2022; Singh & Jeganathan, 2024). However, standard ML models are less suited for raw, high-dimensional inputs such as video feeds or multi-spectral image bands, where CNN and LSTM architectures perform better.", body_style))
    story.append(Paragraph("A major reporting issue in current literature is over-reliance on overall classification accuracy. In imbalanced wildfire datasets—where non-fire areas or non-smoke frames far outnumber positive cases—raw accuracy can give an incomplete picture of model performance. Metrics such as Precision-Recall Area Under Curve (PRC), Cohen's Kappa, and false-positive rates provide clearer performance evaluations.", body_style))
    story.append(Paragraph("In addition, field implementation requires balancing predictive power against reproducibility and processing speed. Models evaluated on private datasets (such as Cao et al., 2019) limit external testing, while resource-intensive deep learning networks require specialized hardware that may not be available in rural fire management facilities.", body_style))

    story.append(Paragraph("7. Limitations of the Present Study", h1_style))
    story.append(Paragraph("This comparative review has three main limitations:", body_style))
    story.append(Paragraph("1. <b>Literature-Based Synthesis:</b> As a review of published studies rather than an analysis of raw datasets, comparisons depend on the specific methods and metrics reported in each paper.", bullet_style))
    story.append(Paragraph("2. <b>Geographic Scope:</b> Reviewed models were developed for specific geographical areas (such as Sydney, Central India, or China), which limits direct application to different forest or climate types.", bullet_style))
    story.append(Paragraph("3. <b>Inconsistent Metrics:</b> Differences in validation methods and reported metrics across studies prevent direct numerical statistical aggregation.", bullet_style))

    story.append(Paragraph("8. Recommendations for Future Research", h1_style))
    story.append(Paragraph("To improve wildfire prediction models for practical deployment, future research should prioritize seven areas:", body_style))
    story.append(Paragraph("• <b>Integrate Real-Time Data Streams:</b> Move from static datasets to continuous inputs, including streaming weather station data, automated satellite observations, and camera networks.", bullet_style))
    story.append(Paragraph("• <b>Include Fuel and Soil Moisture Indicators:</b> Incorporate high-resolution soil moisture data (such as SMAP), fine fuel load measurements, and live fuel moisture observations.", bullet_style))
    story.append(Paragraph("• <b>Combine Physical and Machine Learning Models:</b> Connect data-driven neural networks with physical fire spread formulas (such as Rothermel surface fire equations) to maintain realistic fire behavior.", bullet_style))
    story.append(Paragraph("• <b>Test Across Multiple Regions:</b> Validate predictive models across different climate regions and multi-year fire seasons to test geographical transferability.", bullet_style))
    story.append(Paragraph("• <b>Standardize Model Evaluation Metrics:</b> Require standardized reporting of ROC-AUC, PRC, Kappa, Precision, Recall, F1-Score, and processing latency alongside overall accuracy.", bullet_style))
    story.append(Paragraph("• <b>Support Open Data Initiatives:</b> Publish open, standardized benchmark datasets (combining satellite, weather, and video data) to enable independent testing and model comparison.", bullet_style))
    story.append(Paragraph("• <b>Enhance Model Interpretability:</b> Use explainable AI methods (such as SHAP or LIME) to help fire management personnel understand key factors driving model risk estimates.", bullet_style))

    story.append(Paragraph("9. Conclusion", h1_style))
    story.append(Paragraph("Machine learning, deep learning, GIS, and satellite remote sensing have improved the ability to predict fire occurrence, map regional risk zones, and detect smoke early. Synthesis of current research shows that multimodal hybrid models—combining spatial features (U-Net/CNN) with temporal modeling (LSTM) and multi-layer GIS analysis—provide strong predictive performance across different stages of wildfire management.", body_style))
    story.append(Paragraph("However, practical challenges remain, including static data assumptions, missing fuel variables, private datasets, and limited real-time integration. Addressing these gaps through real-time data inputs, physics-informed models, open benchmark datasets, and interpretable outputs will support the development of practical early warning tools to protect ecosystems, infrastructure, and public safety.", body_style))

    story.append(Spacer(1, 10))
    story.append(Paragraph("Selected References", h1_style))
    refs = [
        "Alkhatib, R., Sahwan, W., Alkhatieb, A., & Schütt, B. (2023). A brief review of machine learning algorithms in forest fires science. <i>Applied Sciences</i>, 13(14), 8275. https://doi.org/10.3390/app13148275",
        "Cao, Y., Yang, F., Tang, Q., & Lu, X. (2019). An attention enhanced bidirectional LSTM for early forest fire smoke recognition. <i>IEEE Access</i>, 7, 154732–154742. https://doi.org/10.1109/ACCESS.2019.2946712",
        "Jaiswal, R. K., Mukherjee, S., Raju, K. D., & Saxena, R. (2002). Forest fire risk zone mapping from satellite imagery and GIS. <i>International Journal of Applied Earth Observation and Geoinformation</i>, 4(1), 1–10. https://doi.org/10.1016/S0303-2434(02)00006-5",
        "Naderpour, M., Rizeei, H. M., & Ramezani, F. (2021). Forest fire risk prediction: A spatial deep neural network-based framework. <i>Remote Sensing</i>, 13(13), 2513. https://doi.org/10.3390/rs13132513",
        "Pang, Y., Li, Y., Feng, Z., Feng, Z., Zhao, Z., Chen, S., & Zhang, H. (2022). Forest fire occurrence prediction in China based on machine learning methods. <i>Remote Sensing</i>, 14(21), 5546. https://doi.org/10.3390/rs14215546",
        "Singh, S. S., & Jeganathan, C. (2024). Using ensemble machine learning algorithm to predict forest fire occurrence probability in Madhya Pradesh and Chhattisgarh, India. <i>Advances in Space Research</i>, 73(4), 2132–2148. https://doi.org/10.1016/j.asr.2023.12.054"
    ]
    for r in refs:
        story.append(Paragraph(f"• {r}", bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF build complete:", filename)

if __name__ == '__main__':
    build_pdf()