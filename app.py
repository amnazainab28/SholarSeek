from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

SCHOLARSHIPS = [
    {
        "id": 1, "title": "HEC Need Based Scholarship", "country": "Pakistan", "amount": "Rs. 50,000 / Year",
        "deadline": "2026-12-31", "level": "Undergraduate", "category": "Need Based",
        "eligibility": "Pakistani student enrolled in HEC recognized public university, family income < Rs. 50,000/month, not receiving any other scholarship.",
        "coverage": "Tuition Fee + Monthly Stipend", "description": "HEC Need Based Scholarship supports financially deserving students so they can complete their degree without financial burden.",
        "link": "https://www.hec.gov.pk", "status": "Open"
    },
    {
        "id": 2, "title": "Ehsaas Undergraduate Scholarship", "country": "Pakistan", "amount": "Full Tuition Fee",
        "deadline": "2026-12-15", "level": "Undergraduate", "category": "Need Based",
        "eligibility": "Low-income family, admitted in public sector university, family income below poverty threshold.",
        "coverage": "100% Tuition Fee + Rs. 4,000 Monthly Stipend", "description": "Pakistan's largest undergraduate program for deserving students from low-income families.",
        "link": "https://www.pass.gov.pk", "status": "Open"
    },
    {
        "id": 3, "title": "PEEF Scholarship Punjab", "country": "Pakistan", "amount": "Rs. 30,000 / Year",
        "deadline": "2027-01-20", "level": "Intermediate / BS", "category": "Merit + Need",
        "eligibility": "Punjab domicile, 60%+ marks in Matric / Inter, monthly family income < Rs. 60,000.",
        "coverage": "Tuition Fee + Monthly Allowance", "description": "Punjab Educational Endowment Fund for talented and needy students of Punjab.",
        "link": "https://www.peef.org.pk", "status": "Open"
    },
    {
        "id": 4, "title": "DAAD Scholarship Germany", "country": "Germany", "amount": "€ 934 / Month",
        "deadline": "2027-08-31", "level": "Masters / PhD", "category": "Fully Funded",
        "eligibility": "Bachelor's degree with 2 years work experience, IELTS 6.5 / TOEFL 90, strong motivation letter.",
        "coverage": "Monthly Payment + Insurance + Travel + Research Allowance", "description": "Germany's most prestigious scholarship for development-related postgraduate courses.",
        "link": "https://www.daad.de", "status": "Open"
    },
    {
        "id": 5, "title": "Chevening Scholarship UK", "country": "United Kingdom", "amount": "Fully Funded",
        "deadline": "2027-11-04", "level": "Masters", "category": "Fully Funded",
        "eligibility": "Undergraduate degree, 2,800+ hours work experience, leadership potential, return to home country for 2 years.",
        "coverage": "Full Tuition + Airfare + Monthly Stipend + Visa", "description": "UK Government's flagship scholarship for future leaders, influencers and decision-makers.",
        "link": "https://www.chevening.org", "status": "Open"
    },
    {
        "id": 6, "title": "Fulbright Scholarship USA", "country": "USA", "amount": "Fully Funded",
        "deadline": "2027-05-15", "level": "Masters / PhD", "category": "Fully Funded",
        "eligibility": "16 years education, GRE required, high academic record, 2-3 recommendation letters.",
        "coverage": "Tuition + Living + Airfare + Health Insurance + Books", "description": "USA's premier exchange program for Pakistani students to study in top US universities.",
        "link": "https://www.usefp.org", "status": "Open"
    },
    {
        "id": 7, "title": "MEXT Scholarship Japan", "country": "Japan", "amount": "¥ 144,000 / Month",
        "deadline": "2027-05-30", "level": "Undergraduate / Research", "category": "Fully Funded",
        "eligibility": "Under 35 years, 16 years education, good academic record, Japanese / English proficiency.",
        "coverage": "Full Tuition + Monthly Allowance + Airfare", "description": "Japanese Government scholarship for international students to study in Japan.",
        "link": "https://www.studyinjapan.go.jp", "status": "Open"
    },
    {
        "id": 8, "title": "Turkey Burslari Scholarship", "country": "Turkey", "amount": "Fully Funded",
        "deadline": "2027-02-20", "level": "BS / MS / PhD", "category": "Fully Funded",
        "eligibility": "Under 21 for BS, under 30 for MS, under 35 for PhD, 70%+ marks for BS, 75%+ for MS/PhD.",
        "coverage": "Tuition + Dormitory + Health + Monthly Stipend + Turkish Course", "description": "Turkey's most competitive scholarship with free Turkish language course for 1 year.",
        "link": "https://www.turkiyeburslari.gov.tr", "status": "Open"
    },
    {
        "id": 9, "title": "Australia Awards Scholarship", "country": "Australia", "amount": "Fully Funded",
        "deadline": "2027-04-30", "level": "Undergraduate / Masters", "category": "Fully Funded",
        "eligibility": "Pakistani citizen, 16 years education, IELTS 6.5, 2 years work experience preferred.",
        "coverage": "Full Tuition + Return Airfare + Living Allowance + Health Cover", "description": "Australian Government scholarship to build skills and leadership in developing countries.",
        "link": "https://www.dfat.gov.au", "status": "Open"
    },
    {
        "id": 10, "title": "Erasmus Mundus Scholarship", "country": "Europe", "amount": "€ 1,400 / Month",
        "deadline": "2027-01-15", "level": "Masters", "category": "Fully Funded",
        "eligibility": "Bachelor's degree, IELTS 6.5, apply to Erasmus Mundus Joint Masters program.",
        "coverage": "Tuition + Travel + Insurance + Monthly Allowance for 24 Months", "description": "Study in 2-3 European countries in one degree, fully funded by European Union.",
        "link": "https://erasmus-plus.ec.europa.eu", "status": "Open"
    },
    {
        "id": 11, "title": "Commonwealth Scholarship UK", "country": "United Kingdom", "amount": "Fully Funded",
        "deadline": "2027-10-15", "level": "Masters / PhD", "category": "Fully Funded",
        "eligibility": "Pakistani citizen, 1st division in Bachelor's, cannot afford UK study without scholarship.",
        "coverage": "Tuition + Airfare + Stipend + Thesis Grant", "description": "UK's scholarship for students from Commonwealth countries for development impact.",
        "link": "https://cscuk.fcdo.gov.uk", "status": "Open"
    },
    {
        "id": 12, "title": "NUST Merit Scholarship", "country": "Pakistan", "amount": "50% Fee Waiver",
        "deadline": "2027-08-10", "level": "Undergraduate", "category": "Merit Based",
        "eligibility": "Admission in NUST, top merit in entry test, maintain CGPA 3.5+.",
        "coverage": "50% Tuition Fee Waiver", "description": "NUST rewards top merit students with fee waivers every semester.",
        "link": "https://www.nust.edu.pk", "status": "Open"
    },
    {
        "id": 13, "title": "LUMS NOP Scholarship", "country": "Pakistan", "amount": "Fully Funded",
        "deadline": "2027-03-15", "level": "Undergraduate", "category": "Need Based",
        "eligibility": "Matric / Inter with 80%+ marks, financially deserving, apply via NOP test.",
        "coverage": "100% Tuition + Hostel + Books + Living", "description": "LUMS National Outreach Program for talented students who cannot afford LUMS.",
        "link": "https://www.lums.edu.pk", "status": "Open"
    },
    {
        "id": 14, "title": "IBA Karachi Scholarship", "country": "Pakistan", "amount": "Rs. 100,000 / Semester",
        "deadline": "2027-06-30", "level": "Undergraduate", "category": "Merit + Need",
        "eligibility": "Admission in IBA, family income proof, good academic record.",
        "coverage": "Partial to Full Fee Waiver based on need", "description": "IBA financial assistance program for deserving students.",
        "link": "https://www.iba.edu.pk", "status": "Open"
    },
        {
        "id": 15, "title": "Chinese Government Scholarship (CSC)", "country": "China", "amount": "Fully Funded",
        "deadline": "2027-03-31", "level": "BS / Masters / PhD", "category": "Fully Funded",
        "eligibility": "Under 25 for BS, under 35 for MS, under 40 for PhD, 70%+ marks, HSK / IELTS accepted.",
        "coverage": "Full Tuition + Free Dormitory + Monthly Stipend 2500-3500 CNY + Medical Insurance",
        "description": "China's largest scholarship to study in 270+ Chinese universities. No application fee.",
        "link": "https://www.campuschina.org", "status": "Open"
    },
    {
        "id": 16, "title": "Korean Government Scholarship (GKS)", "country": "South Korea", "amount": "Fully Funded",
        "deadline": "2027-02-28", "level": "Undergraduate / Masters / PhD", "category": "Fully Funded",
        "eligibility": "Under 25 for BS, under 40 for MS/PhD, CGPA 2.64/4.0+, good health, English / Korean proficiency.",
        "coverage": "Full Tuition + Airfare + 900,000 KRW Monthly + Settlement + 1 Year Korean Language Course",
        "description": "Korea's most famous scholarship with 1 year free Korean language training.",
        "link": "https://www.studyinkorea.go.kr", "status": "Open"
    },
    {
        "id": 17, "title": "Eiffel Excellence Scholarship France", "country": "France", "amount": "€ 1,181 / Month",
        "deadline": "2027-01-08", "level": "Masters / PhD", "category": "Fully Funded",
        "eligibility": "Under 25 for Masters, under 30 for PhD, apply through French university, excellent academic record.",
        "coverage": "Monthly Allowance + Travel + Insurance + Cultural Activities (Tuition not included)",
        "description": "French Government scholarship for top international students in top French universities.",
        "link": "https://www.campusfrance.org", "status": "Open"
    },
    {
        "id": 18, "title": "Holland Scholarship Netherlands", "country": "Netherlands", "amount": "€ 5,000",
        "deadline": "2027-02-01", "level": "Undergraduate / Masters", "category": "Partial Funded",
        "eligibility": "Non-EEA student, admitted to Dutch research university, IELTS 6.5+, first time in Netherlands.",
        "coverage": "€ 5,000 One Time Grant + Tuition Discount in some universities",
        "description": "Dutch Government scholarship for international students outside Europe.",
        "link": "https://www.studyinnl.org", "status": "Open"
    },
    {
        "id": 19, "title": "Swedish Institute Scholarship (SI)", "country": "Sweden", "amount": "Fully Funded",
        "deadline": "2027-02-28", "level": "Masters", "category": "Fully Funded",
        "eligibility": "Pakistani citizen, 3,000 hours work experience, leadership experience, admitted to SI-eligible Masters.",
        "coverage": "Full Tuition + SEK 12,000 Monthly + Travel Grant + Insurance",
        "description": "Sweden Government scholarship for future global leaders from developing countries.",
        "link": "https://si.se", "status": "Open"
    },
    {
        "id": 20, "title": "Swiss Government Excellence Scholarship", "country": "Switzerland", "amount": "CHF 1,920 / Month",
        "deadline": "2027-09-30", "level": "Masters / PhD / Postdoc", "category": "Fully Funded",
        "eligibility": "Masters degree, under 35, research proposal, professor acceptance letter from Swiss university.",
        "coverage": "Monthly Payment + Tuition Waiver + Health Insurance + Airfare + Housing Allowance",
        "description": "Switzerland's most prestigious scholarship for research in Swiss universities.",
        "link": "https://www.sbfi.admin.ch", "status": "Open"
    },
    {
        "id": 21, "title": "Gates Cambridge Scholarship", "country": "United Kingdom", "amount": "Fully Funded",
        "deadline": "2027-12-03", "level": "Masters / PhD", "category": "Fully Funded",
        "eligibility": "Admission to Cambridge University, outstanding academic + leadership + commitment to improve lives.",
        "coverage": "Full Tuition + £21,000 Yearly Stipend + Airfare + Visa + Research Grant",
        "description": "Bill Gates Foundation scholarship to study at University of Cambridge.",
        "link": "https://www.gatescambridge.org", "status": "Open"
    },
    {
        "id": 22, "title": "Rhodes Scholarship Oxford", "country": "United Kingdom", "amount": "Fully Funded",
        "deadline": "2027-08-01", "level": "Masters / PhD", "category": "Fully Funded",
        "eligibility": "Age 19-25, Bachelor's degree with high merit, leadership + character, 2 years in Pakistan.",
        "coverage": "Full Oxford Tuition + £19,092 Yearly Stipend + Airfare + Visa",
        "description": "World's oldest and most prestigious scholarship to study at Oxford University.",
        "link": "https://www.rhodeshouse.ox.ac.uk", "status": "Open"
    },
    {
        "id": 23, "title": "SINGA Scholarship Singapore", "country": "Singapore", "amount": "S$ 2,700 / Month",
        "deadline": "2027-06-01", "level": "PhD", "category": "Fully Funded",
        "eligibility": "Bachelor's / Masters in Science / Engineering, IELTS 6.5, strong research interest, under 35.",
        "coverage": "Full Tuition + Monthly Stipend + Airfare + Settlement Allowance for 4 Years",
        "description": "Singapore's PhD scholarship to study in NUS, NTU, SUTD with A*STAR labs.",
        "link": "https://www.a-star.edu.sg", "status": "Open"
    },
    {
        "id": 24, "title": "Qatar University Scholarship", "country": "Qatar", "amount": "Fully Funded",
        "deadline": "2027-03-10", "level": "Undergraduate", "category": "Fully Funded",
        "eligibility": "High school with 95%+ marks, IELTS 6.0, good conduct, under 25 years.",
        "coverage": "Full Tuition + Free Hostel + Monthly Stipend + Yearly Air Ticket",
        "description": "Qatar University scholarship for outstanding international students.",
        "link": "https://www.qu.edu.qa", "status": "Open"
    },
]

@app.route("/")
def home():
    search = request.args.get("search", "").lower()
    country = request.args.get("country", "")
    level = request.args.get("level", "")
    
    filtered = SCHOLARSHIPS
    if search:
        filtered = [s for s in filtered if search in s["title"].lower() or search in s["country"].lower()]
    if country:
        filtered = [s for s in filtered if s["country"] == country]
    if level:
        filtered = [s for s in filtered if level in s["level"]]
    
    countries = sorted(set(s["country"] for s in SCHOLARSHIPS))
    return render_template("index.html", scholarships=filtered, countries=countries, total=len(SCHOLARSHIPS), now=datetime.now().strftime("%d %B %Y"))

@app.route("/scholarship/<int:sid>")
def detail(sid):
    s = next((x for x in SCHOLARSHIPS if x["id"] == sid), None)
    return render_template("detail.html", s=s) if s else ("Not Found", 404)

if __name__ == "__main__":
    import os
app.secret_key = os.environ.get("SECRET_KEY", "change-this-to-a-long-random-key-12345")
import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port, debug=False)
