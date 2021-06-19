from flask import Flask ,request , render_template , jsonify ,Response ,redirect
from flask.helpers import flash, url_for
import json
from db import insert_one,find_one,delete_many,update
import pickle
from functools import wraps
import wikipedia
import datetime

app=Flask(__name__)
app.config['SECRET_KEY']='asdhfbdsf3jwio'

g_user=""

def login_required(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if g_user:
                return f(*args, **kwargs)
            else:
                flash('Buddy ,You need to login first.')
                return redirect(url_for('login'))

        return wrap
 




@app.route("/")
def home():
    return render_template("home.html")

@app.route("/logout")
def logout():
    global g_user 
    g_user=None
    return redirect(url_for("home"))

@app.route("/login",methods=['GET','POST'])
def login():
    if(request.method=='POST'):
        global g_user
        email=request.form['email']
        password=request.form['password']
        # g_email=email
        user=find_one(email)
        if(user!=None):
            g_user=user
            print("g_user=",g_user)
            return redirect(url_for("disease_predict"))
        return render_template("login.html",msg="User Does not exist")
        
        
    return render_template("login.html")


@app.route("/disease_predict")
@login_required
def disease_predict():
    global g_user
    return render_template("disease_pred.html",user=g_user)

@app.route("/signin",methods=['GET','POST'])
def signin():
    if(request.method=='POST'):
        email=request.form['email']
        password=request.form['password']
        try:
            insert_one(email=email,password=password)
            return render_template("login.html",msg="succesfull signin")
        except:
            return render_template("login.html",msg="failed to signin")

    return render_template("login.html")




@app.route('/_autocomplete', methods=['GET'])
def autocomplete():
    symptoms = ['shortness of breath', 'dizziness', 'asthenia', 'fall', 'syncope',
       'vertigo', 'sweat', 'sweating increased', 'palpitation', 'nausea',
       'angina pectoris', 'pressure chest', 'polyuria', 'polydypsia',
       'pain chest', 'orthopnea', 'rale', 'unresponsiveness',
       'mental status changes', 'vomiting', 'labored breathing',
       'feeling suicidal', 'suicidal', 'hallucinations auditory',
       'feeling hopeless', 'weepiness', 'sleeplessness',
       'motor retardation', 'irritable mood', 'blackout',
       'mood depressed', 'hallucinations visual', 'worry', 'agitation',
       'tremor', 'intoxication', 'verbal auditory hallucinations',
       'energy increased', 'difficulty', 'nightmare',
       'unable to concentrate', 'homelessness', 'hypokinesia',
       'dyspnea on exertion', 'chest tightness', 'cough', 'fever',
       'decreased translucency', 'productive cough', 'pleuritic pain',
       'yellow sputum', 'breath sounds decreased', 'chill', 'rhonchus',
       'green sputum', 'non-productive cough', 'wheezing', 'haemoptysis',
       'distress respiratory', 'tachypnea', 'malaise', 'night sweat',
       'jugular venous distention', 'dyspnea', 'dysarthria',
       'speech slurred', 'facial paresis', 'hemiplegia', 'seizure',
       'numbness', 'symptom aggravating factors', 'st segment elevation',
       'st segment depression', 't wave inverted', 'presence of q wave',
       'chest discomfort', 'bradycardia', 'pain', 'nonsmoker', 'erythema',
       'hepatosplenomegaly', 'pruritus', 'diarrhea', 'abscess bacterial',
       'swelling', 'apyrexial', 'dysuria', 'hematuria',
       'renal angle tenderness', 'lethargy', 'hyponatremia',
       'hemodynamically stable', 'difficulty passing urine',
       'consciousness clear', 'guaiac positive', 'monoclonal',
       'ecchymosis', 'tumor cell invasion', 'haemorrhage', 'pallor',
       'fatigue', 'heme positive', 'pain back', 'orthostasis',
       'arthralgia', 'transaminitis', 'sputum purulent', 'hypoxemia',
       'hypercapnia', 'patient non compliance', 'unconscious state',
       'bedridden', 'abdominal tenderness', 'unsteady gait',
       'hyperkalemia', 'urgency of\xa0micturition', 'ascites',
       'hypotension', 'enuresis', 'asterixis', 'muscle twitch', 'sleepy',
       'headache', 'lightheadedness', 'food intolerance',
       'numbness of hand', 'general discomfort', 'drowsiness',
       'stiffness', 'prostatism', 'weight gain', 'tired',
       'mass of body structure', 'has religious belief', 'nervousness',
       'formication', 'hot flush', 'lesion', 'cushingoid facies',
       'cushingoid\xa0habitus', 'emphysematous change',
       'decreased body weight', 'hoarseness', 'thicken',
       'spontaneous rupture of membranes', 'muscle hypotonia',
       'hypotonic', 'redness', 'hypesthesia', 'hyperacusis',
       'scratch marks', 'sore to touch', 'burning sensation',
       'satiety early', 'throbbing sensation quality',
       'sensory discomfort', 'constipation', 'pain abdominal',
       'heartburn', 'breech presentation', 'cyanosis',
       'pain in lower limb', 'cardiomegaly', 'clonus', 'unwell',
       'anorexia', 'history of - blackout', 'anosmia',
       'metastatic lesion', 'hemianopsia homonymous',
       'hematocrit decreased', 'neck stiffness', 'cicatrisation',
       'hypometabolism', 'aura', 'myoclonus', 'gurgle',
       'wheelchair bound', 'left\xa0atrial\xa0hypertrophy', 'oliguria',
       'catatonia', 'unhappy', 'paresthesia', 'gravida 0', 'lung nodule',
       'distended abdomen', 'ache', 'macerated skin', 'heavy feeling',
       'rest pain', 'sinus rhythm', 'withdraw', 'behavior hyperactive',
       'terrify', 'photopsia', 'giddy mood', 'disturbed family',
       'hypersomnia', 'hyperhidrosis disorder', 'mydriasis',
       'extrapyramidal sign', 'loose associations', 'exhaustion', 'snore',
       'r wave feature', 'overweight', 'systolic murmur', 'asymptomatic',
       'splenomegaly', 'bleeding of vagina', 'macule', 'photophobia',
       'painful swallowing', 'cachexia', 'hypocalcemia result',
       'hypothermia, natural', 'atypia', 'general unsteadiness',
       'throat sore', 'snuffle', 'hacking cough', 'stridor', 'paresis',
       'aphagia', 'focal seizures', 'abnormal sensation', 'stupor',
       'fremitus', "Stahli's line", 'stinging sensation', 'paralyse',
       'hirsutism', 'sniffle', 'bradykinesia', 'out of breath',
       'urge incontinence', 'vision blurred', 'room spinning',
       'rambling speech', 'clumsiness', 'decreased stool caliber',
       'hematochezia', 'egophony', 'scar tissue', 'neologism',
       'decompensation', 'stool color yellow',
       'rigor - temperature-associated observation', 'paraparesis',
       'moody', 'fear of falling', 'spasm', 'hyperventilation',
       'excruciating pain', 'gag', 'posturing', 'pulse absent',
       'dysesthesia', 'polymyalgia', 'passed stones',
       'qt interval prolonged', 'ataxia', "Heberden's node",
       'hepatomegaly', 'sciatica', 'frothy sputum', 'mass in breast',
       'retropulsion', 'estrogen use', 'hypersomnolence', 'underweight',
       'dullness', 'red blotches', 'colic abdominal', 'hypokalemia',
       'hunger', 'prostate tender', 'pain foot', 'urinary hesitation',
       'disequilibrium', 'flushing', 'indifferent mood', 'urinoma',
       'hypoalbuminemia', 'pustule', 'slowing of urinary stream',
       'extreme exhaustion', 'no status change', 'breakthrough pain',
       'pansystolic murmur', 'systolic ejection murmur', 'stuffy nose',
       'barking cough', 'rapid shallow breathing', 'noisy respiration',
       'nasal discharge present', 'frail', 'cystic lesion',
       'projectile vomiting', 'heavy legs', 'titubation',
       'dysdiadochokinesia', 'achalasia', 'side pain', 'monocytosis',
       'posterior\xa0rhinorrhea', 'incoherent', 'lameness',
       'claudication', 'clammy skin', 'mediastinal shift',
       'nausea and vomiting', 'awakening early', 'tenesmus', 'fecaluria',
       'pneumatouria', 'todd paralysis', 'alcoholic withdrawal symptoms',
       'myalgia', 'dyspareunia', 'poor dentition', 'floppy',
       'inappropriate affect', 'poor feeding', 'moan', 'welt', 'tinnitus',
       'hydropneumothorax', 'superimposition', 'feeling strange',
       'uncoordination', 'absences finding', 'tonic seizures',
       'debilitation', 'impaired cognition', 'drool', 'pin-point pupils',
       'tremor resting', 'groggy', 'adverse reaction', 'adverse effect',
       'abdominal bloating', 'fatigability', 'para 2', 'abortion',
       'intermenstrual heavy bleeding', 'previous pregnancies 2',
       'primigravida', 'abnormally hard consistency', 'proteinemia',
       'pain neck', 'dizzy spells', 'shooting pain', 'hyperemesis',
       'milky', 'regurgitates after swallowing', 'lip smacking',
       'phonophobia', 'rolling of eyes', 'ambidexterity',
       'pulsus\xa0paradoxus', 'gravida 10', 'bruit',
       'breath-holding spell', 'scleral\xa0icterus', 'retch', 'blanch',
       'elation', 'verbally abusive behavior', 'transsexual',
       'behavior showing increased motor activity',
       'coordination abnormal', 'choke', 'bowel sounds decreased',
       'no known drug allergies', 'low back pain', 'charleyhorse',
       'sedentary', 'feels hot/feverish', 'flare',
       'pericardial friction rub', 'hoard', 'panic',
       'cardiovascular finding', 'cardiovascular event',
       'soft tissue swelling', 'rhd positive', 'para 1', 'nasal flaring',
       'sneeze', 'hypertonicity', "Murphy's sign", 'flatulence',
       'gasping for breath', 'feces in rectum', 'prodrome',
       'hypoproteinemia', 'alcohol binge episode', 'abdomen acute',
       'air fluid level', 'catching breath', 'large-for-dates fetus',
       'immobile', 'homicidal thoughts']
    # print(cities)    
    return Response(json.dumps(symptoms), mimetype='application/json')
 
#create enumerate dict
symptoms = ['shortness of breath', 'dizziness', 'asthenia', 'fall', 'syncope',
       'vertigo', 'sweat', 'sweating increased', 'palpitation', 'nausea',
       'angina pectoris', 'pressure chest', 'polyuria', 'polydypsia',
       'pain chest', 'orthopnea', 'rale', 'unresponsiveness',
       'mental status changes', 'vomiting', 'labored breathing',
       'feeling suicidal', 'suicidal', 'hallucinations auditory',
       'feeling hopeless', 'weepiness', 'sleeplessness',
       'motor retardation', 'irritable mood', 'blackout',
       'mood depressed', 'hallucinations visual', 'worry', 'agitation',
       'tremor', 'intoxication', 'verbal auditory hallucinations',
       'energy increased', 'difficulty', 'nightmare',
       'unable to concentrate', 'homelessness', 'hypokinesia',
       'dyspnea on exertion', 'chest tightness', 'cough', 'fever',
       'decreased translucency', 'productive cough', 'pleuritic pain',
       'yellow sputum', 'breath sounds decreased', 'chill', 'rhonchus',
       'green sputum', 'non-productive cough', 'wheezing', 'haemoptysis',
       'distress respiratory', 'tachypnea', 'malaise', 'night sweat',
       'jugular venous distention', 'dyspnea', 'dysarthria',
       'speech slurred', 'facial paresis', 'hemiplegia', 'seizure',
       'numbness', 'symptom aggravating factors', 'st segment elevation',
       'st segment depression', 't wave inverted', 'presence of q wave',
       'chest discomfort', 'bradycardia', 'pain', 'nonsmoker', 'erythema',
       'hepatosplenomegaly', 'pruritus', 'diarrhea', 'abscess bacterial',
       'swelling', 'apyrexial', 'dysuria', 'hematuria',
       'renal angle tenderness', 'lethargy', 'hyponatremia',
       'hemodynamically stable', 'difficulty passing urine',
       'consciousness clear', 'guaiac positive', 'monoclonal',
       'ecchymosis', 'tumor cell invasion', 'haemorrhage', 'pallor',
       'fatigue', 'heme positive', 'pain back', 'orthostasis',
       'arthralgia', 'transaminitis', 'sputum purulent', 'hypoxemia',
       'hypercapnia', 'patient non compliance', 'unconscious state',
       'bedridden', 'abdominal tenderness', 'unsteady gait',
       'hyperkalemia', 'urgency of\xa0micturition', 'ascites',
       'hypotension', 'enuresis', 'asterixis', 'muscle twitch', 'sleepy',
       'headache', 'lightheadedness', 'food intolerance',
       'numbness of hand', 'general discomfort', 'drowsiness',
       'stiffness', 'prostatism', 'weight gain', 'tired',
       'mass of body structure', 'has religious belief', 'nervousness',
       'formication', 'hot flush', 'lesion', 'cushingoid facies',
       'cushingoid\xa0habitus', 'emphysematous change',
       'decreased body weight', 'hoarseness', 'thicken',
       'spontaneous rupture of membranes', 'muscle hypotonia',
       'hypotonic', 'redness', 'hypesthesia', 'hyperacusis',
       'scratch marks', 'sore to touch', 'burning sensation',
       'satiety early', 'throbbing sensation quality',
       'sensory discomfort', 'constipation', 'pain abdominal',
       'heartburn', 'breech presentation', 'cyanosis',
       'pain in lower limb', 'cardiomegaly', 'clonus', 'unwell',
       'anorexia', 'history of - blackout', 'anosmia',
       'metastatic lesion', 'hemianopsia homonymous',
       'hematocrit decreased', 'neck stiffness', 'cicatrisation',
       'hypometabolism', 'aura', 'myoclonus', 'gurgle',
       'wheelchair bound', 'left\xa0atrial\xa0hypertrophy', 'oliguria',
       'catatonia', 'unhappy', 'paresthesia', 'gravida 0', 'lung nodule',
       'distended abdomen', 'ache', 'macerated skin', 'heavy feeling',
       'rest pain', 'sinus rhythm', 'withdraw', 'behavior hyperactive',
       'terrify', 'photopsia', 'giddy mood', 'disturbed family',
       'hypersomnia', 'hyperhidrosis disorder', 'mydriasis',
       'extrapyramidal sign', 'loose associations', 'exhaustion', 'snore',
       'r wave feature', 'overweight', 'systolic murmur', 'asymptomatic',
       'splenomegaly', 'bleeding of vagina', 'macule', 'photophobia',
       'painful swallowing', 'cachexia', 'hypocalcemia result',
       'hypothermia, natural', 'atypia', 'general unsteadiness',
       'throat sore', 'snuffle', 'hacking cough', 'stridor', 'paresis',
       'aphagia', 'focal seizures', 'abnormal sensation', 'stupor',
       'fremitus', "Stahli's line", 'stinging sensation', 'paralyse',
       'hirsutism', 'sniffle', 'bradykinesia', 'out of breath',
       'urge incontinence', 'vision blurred', 'room spinning',
       'rambling speech', 'clumsiness', 'decreased stool caliber',
       'hematochezia', 'egophony', 'scar tissue', 'neologism',
       'decompensation', 'stool color yellow',
       'rigor - temperature-associated observation', 'paraparesis',
       'moody', 'fear of falling', 'spasm', 'hyperventilation',
       'excruciating pain', 'gag', 'posturing', 'pulse absent',
       'dysesthesia', 'polymyalgia', 'passed stones',
       'qt interval prolonged', 'ataxia', "Heberden's node",
       'hepatomegaly', 'sciatica', 'frothy sputum', 'mass in breast',
       'retropulsion', 'estrogen use', 'hypersomnolence', 'underweight',
       'dullness', 'red blotches', 'colic abdominal', 'hypokalemia',
       'hunger', 'prostate tender', 'pain foot', 'urinary hesitation',
       'disequilibrium', 'flushing', 'indifferent mood', 'urinoma',
       'hypoalbuminemia', 'pustule', 'slowing of urinary stream',
       'extreme exhaustion', 'no status change', 'breakthrough pain',
       'pansystolic murmur', 'systolic ejection murmur', 'stuffy nose',
       'barking cough', 'rapid shallow breathing', 'noisy respiration',
       'nasal discharge present', 'frail', 'cystic lesion',
       'projectile vomiting', 'heavy legs', 'titubation',
       'dysdiadochokinesia', 'achalasia', 'side pain', 'monocytosis',
       'posterior\xa0rhinorrhea', 'incoherent', 'lameness',
       'claudication', 'clammy skin', 'mediastinal shift',
       'nausea and vomiting', 'awakening early', 'tenesmus', 'fecaluria',
       'pneumatouria', 'todd paralysis', 'alcoholic withdrawal symptoms',
       'myalgia', 'dyspareunia', 'poor dentition', 'floppy',
       'inappropriate affect', 'poor feeding', 'moan', 'welt', 'tinnitus',
       'hydropneumothorax', 'superimposition', 'feeling strange',
       'uncoordination', 'absences finding', 'tonic seizures',
       'debilitation', 'impaired cognition', 'drool', 'pin-point pupils',
       'tremor resting', 'groggy', 'adverse reaction', 'adverse effect',
       'abdominal bloating', 'fatigability', 'para 2', 'abortion',
       'intermenstrual heavy bleeding', 'previous pregnancies 2',
       'primigravida', 'abnormally hard consistency', 'proteinemia',
       'pain neck', 'dizzy spells', 'shooting pain', 'hyperemesis',
       'milky', 'regurgitates after swallowing', 'lip smacking',
       'phonophobia', 'rolling of eyes', 'ambidexterity',
       'pulsus\xa0paradoxus', 'gravida 10', 'bruit',
       'breath-holding spell', 'scleral\xa0icterus', 'retch', 'blanch',
       'elation', 'verbally abusive behavior', 'transsexual',
       'behavior showing increased motor activity',
       'coordination abnormal', 'choke', 'bowel sounds decreased',
       'no known drug allergies', 'low back pain', 'charleyhorse',
       'sedentary', 'feels hot/feverish', 'flare',
       'pericardial friction rub', 'hoard', 'panic',
       'cardiovascular finding', 'cardiovascular event',
       'soft tissue swelling', 'rhd positive', 'para 1', 'nasal flaring',
       'sneeze', 'hypertonicity', "Murphy's sign", 'flatulence',
       'gasping for breath', 'feces in rectum', 'prodrome',
       'hypoproteinemia', 'alcohol binge episode', 'abdomen acute',
       'air fluid level', 'catching breath', 'large-for-dates fetus',
       'immobile', 'homicidal thoughts']

disease_dict={}
for key,val in enumerate(symptoms):
    disease_dict[val]=key

@app.route("/symptoms")
def smptoms():
    global symptoms
    return render_template("symptoms.html",symptoms=symptoms)


@app.route("/predict", methods=['GET','POST'])
@login_required
def predict():
    global disease_dict
    if(request.method=='POST'):
        arr=[]
        len=request.form['length']
        print(type(len))
        for i in range(0,int(len)):
            arr.append(request.form['symptom{}'.format(i)])
        # print(list(arr))
        # print(len(list(arr)))  
        #array for pos
        pos=[]
        for symp in arr:
            if(symp in disease_dict):
                pos.append(disease_dict[symp])
        
        print(pos) 

        #predict diseases
        filename='decision_tree_model.sav'
        loaded_model = pickle.load(open(filename, 'rb'))
        inp=[0.0]*404
        for i in pos:
            inp[i]=1.0
        result = loaded_model.predict([inp])
        result1=result[0]   #result1 is string
        resp=str(result)
        resp1=result1.replace("\xa0"," ")
        global g_user
        print(resp," ",resp1)
        #update into the database history
        resp_tuple=(resp1,str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")),arr)
        update(g_user['email'],resp_tuple)

        
        try:
            wiki_result=wikipedia.summary(resp)
        except:
            wiki_result="We dont have information about it!Sorry!!!"

        g_user=find_one(g_user['email'])
        responce={
            'user':g_user,
            'result':result[0],
            'wiki':wiki_result
        }
        
        return render_template("result.html",responce=responce,user=g_user)


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/history")
def history():
    global g_user
    return render_template("history.html",user=g_user)

if(__name__=='__main__'):
    app.run(port=3001,debug=True)
