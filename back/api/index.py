import datetime
import json
import operator
import time

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.paginator import Paginator
from django.db.models import Q, Count, F
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.utils.termcolors import background
from django.views.decorators.csrf import csrf_exempt

from back.models import *
from back.form import *
from django.core.files.storage import default_storage
from back.utils import Tools
from django.core.exceptions import ObjectDoesNotExist
from back.utils.decorators import get_user_from_session, has_permission
from django.views.decorators.clickjacking import xframe_options_sameorigin
from back.models import *
from django.http import JsonResponse
from django.views import View
from dwebsocket import accept_websocket, require_websocket
from back.utils.data_init import run
from back.utils.data2sql import run_sql
from back.utils.predict_model import model_ceshi
clients={}
ALL_CITIES_LNG_LAT ={'三亚': [109.51855670139908, 18.258736291747855], '三明': [117.64552116782143, 26.269736515991838], '三门峡': [111.2065332238741, 34.778327249459984], '上海': [121.48053886017651, 31.235929042252014], '上饶': [117.94945960312224, 28.460625921851733], '东莞': [113.75842045787648, 23.02730841164339], '东营': [118.58846268606544, 37.45484732016579], '中山': [121.65154739366945, 38.92451111549568], '临汾': [111.52553022403073, 36.093741895419726], '临沂': [118.36353300501388, 35.11067124236514], '丹东': [124.36154728159079, 40.00640870559368], '丽水': [119.9295730584414, 28.473278180563412], '乌兰察布': [113.13946767446333, 41.00074832767381], '乌鲁木齐': [87.62443993536046, 43.830763204290484], '乐山': [103.7725376036347, 29.55794071745811], '九江': [116.00753491163063, 29.711340559079343], '云浮': [112.05151269959146, 22.920911970342857], '五指山': [109.52354032070569, 18.780994100706135], '亳州': [115.7844632112745, 33.850642695788835], '伊犁': [], '佛山': [113.12851219549718, 23.02775875078891], '佳木斯': [130.327359092573, 46.80568999085779], '俄罗斯联邦': [126.63279440302125, 45.77443571637344], '保定': [115.47146383768579, 38.87998776845534], '信阳': [114.09748283304512, 32.15301454753105], '儋州': [109.58745583568611, 19.527146110044196], '克孜勒苏': [78.542164705457, 41.1456526081493], '克拉玛依': [84.866221962114, 45.596624206980934], '六安': [116.52640966418569, 31.741450815322555], '兰州': [103.84052119633628, 36.067234693545565], '兴平': [108.49639400876816, 34.30547652029205], '其他': [122.1680354229059, 40.72495580033915], '内江': [105.06458802499718, 29.58588653832045], '包头': [109.84654350721243, 40.66292878826139], '北京': [116.4133836971231, 39.910924547299565], '北海': [109.126533212566, 21.48683649576942], '十堰': [110.80452956069568, 32.63506185840116], '南京': [118.80242172124585, 32.06465288561847], '南充': [106.11750261487227, 30.843782508337036], '南宁': [108.37345082581861, 22.822606601187154], '南平': [118.1843695481426, 26.647772874203266], '南昌': [115.86458944231661, 28.68945529506072], '南通': [120.90159173866185, 31.98654943120089], '南阳': [112.53450131351325, 32.99656220465144], '印度': [], '印度尼西亚': [], '厦门': [118.09643549976651, 24.485406605176305], '台州': [121.42743470427969, 28.66219405599615], '合肥': [117.23344266497664, 31.826577833686887], '吉安': [115.00051072001253, 27.119726826070448], '吉林市': [126.55563450495482, 43.84356783457924], '吕梁': [111.15044967529185, 37.524497749577115], '周口': [114.70348251482332, 33.6318288757022], '呼伦贝尔': [119.77237049946636, 49.21844647556481], '呼和浩特': [111.75550856170946, 40.84842299711348], '和田': [79.92021246975499, 37.11833554446567], '咸宁': [114.32851909026844, 29.847055947646492], '咸阳': [108.71542245143303, 34.335476293368586], '哈尔滨': [126.54161509031663, 45.808825827952184], '唐山': [118.18645947203979, 39.63658372414733], '商丘': [115.66244933826238, 34.4202016658586], '喀什': [76.00031273791514, 39.47364953291228], '嘉兴': [120.76355182586005, 30.750974830920143], '嘉峪关': [98.29620384300111, 39.77796014739059], '四平': [124.35648155715893, 43.171993571561], '国外': [], '大庆': [125.10865763402039, 46.59363317672175], '大连': [121.62163148459285, 38.9189536667856], '天水': [105.73141674566955, 34.58741188165064], '天津': [117.21081309155257, 39.143929903310074], '太仓市': [121.13559529350024, 31.464599352977785], '太原': [112.55639149167204, 37.87698902884778], '威海': [122.12754097831325, 37.5164305480148], '娄底': [112.00150349288418, 27.703208596991583], '孝感': [113.92251007733665, 30.930689227018295], '宁德': [119.55451074542829, 26.672241711408567], '宁波': [121.62857249434141, 29.866033045866054], '安庆': [117.06360390491879, 30.53095656804304], '安康': [109.03560108265746, 32.69051277057377], '安阳': [114.39950042177432, 36.10594098401491], '安顺': [105.95441712388904, 26.25925237871499], '宜宾': [104.6494037048691, 28.75800702855183], '宜昌': [111.29254921035434, 30.697446484492378], '宜春': [114.4235636759064, 27.820856421848216], '宝鸡': [107.2445753670404, 34.36891564286998], '宣城': [118.76553424276743, 30.94660154529291], '宿迁': [118.28157403570837, 33.96774971569008], '岳阳': [113.13548942422142, 29.3631782939259], '峨眉': [109.33593712009724, 22.49546949018848], '巴中': [106.7515853031645, 31.872888585956545], '巴彦淖尔': [107.39439808372491, 40.7493594895728], '常州': [119.98148471327892, 31.815795653327836], '常德': [111.70545217995837, 29.037749999406877], '常熟': [120.75949588665195, 31.65953827674108], '平顶山': [113.19952856052156, 33.772050748691015], '广元': [105.85042318166482, 32.44161630531542], '广安': [106.64853115607652, 30.479768100141722], '广州': [113.27143134445974, 23.135336306695006], '廊坊': [116.69058173342549, 39.54336666275853], '延安': [109.49658191612687, 36.59111103521779], '延边': [129.4773763202274, 42.91574303372181], '开封': [114.31459258497121, 34.80288581121172], '张家口': [114.89257223145165, 40.7732372026915], '张家港': [120.56155363871446, 31.88114053634028], '张家界': [110.48553254695402, 29.122815562551878], '徐州': [117.29057543439453, 34.21266655011306], '德国': [], '德州': [116.36555674397471, 37.441308454576266], '德阳': [104.40441936496448, 31.133115003656755], '怀化': [110.00851426537254, 27.575160902978517], '惠州': [114.4235580165817, 23.116358854725593], '成都': [104.08153351042463, 30.655821878416408], '扬州': [119.41941890822997, 32.40067693609037], '承德': [117.96939750996681, 40.95785601233803], '抚顺': [123.9643746156145, 41.88596959305694], '拉萨': [91.12082391546393, 29.65004027476773], '揭阳': [116.37851218033846, 23.555740488275585], '新乡': [113.93360046733228, 35.3096399303368], '新余': [114.9235346513963, 27.823578697788587], '新加坡': [105.96171430208666, 26.258323531902303], '方家山': [119.1121804388429, 32.06948272415697], '无锡': [120.31858328810601, 31.498809732685714], '日喀则': [88.89370303482552, 29.275657822511512], '日本': [99.77874898872787, 32.7983219757217], '日照': [119.53341540456555, 35.42283899843767], '昆山': [120.98745249794995, 31.390863425081864], '昆明': [102.85244836500482, 24.873998150044006], '晋中': [112.75959475565928, 37.69283940975972], '晋城': [112.85857823132879, 35.49628458647257], '普洱': [100.97256981472799, 22.830979186010275], '景德镇': [117.18457644638579, 29.274247711040953], '曲靖': [103.80243482794681, 25.496406931543667], '朝阳': [116.44955872950158, 39.926374523079886], '杭州': [120.21551180372168, 30.25308298169347], '松原': [124.83148187569292, 45.14740419341382], '枣庄': [117.33054194483897, 34.815994048435115], '柬埔寨': [108.40012933165896, 22.827430839873834], '柳州': [109.43442194634564, 24.331961386852413], '株洲': [113.14047079776427, 27.833567639016444], '桂林': [110.20354537457943, 25.242885724872647], '梅州': [116.12953737612247, 24.294177532206206], '榆林': [109.74161603381395, 38.290883835484046], '武汉': [114.31158155473231, 30.598466736400987], '毕节': [105.33332337116845, 27.408562131330886], '永州': [111.61945505792227, 26.425864117900094], '汕头': [116.68852864054833, 23.35909171772515], '汕尾': [115.3729242893998, 22.77873050016389], '江门': [113.08855619524043, 22.584603880965], '池州': [117.49842096159624, 30.670883790764535], '沈阳': [123.4559899308919, 41.720915668888956], '沧州': [116.84558075595014, 38.310215141107044], '河源': [114.70744627290641, 23.749684370959752], '泉州': [118.68244626680422, 24.879952330498313], '泰安': [117.0944948347959, 36.2058580448846], '泰州': [119.9295663378548, 32.4606750493083], '泸州': [105.4485240693266, 28.87766830360723], '洛阳': [112.4594212983115, 34.62426277921943], '济南': [117.12639941261048, 36.65655420178723], '济宁': [116.59361234853988, 35.420177394529645], '济源': [112.60858070620743, 35.072907226846525], '海东': [102.1104440722824, 36.508511080941304], '海口': [110.32552547126409, 20.04404943925674], '淄博': [118.06145253489896, 36.81908568332188], '淮北': [116.8045372670298, 33.96165630027632], '淮南': [117.00638885071616, 32.63184739905333], '淮安': [119.14746320322271, 33.508999838207515], '深圳': [114.06455183658751, 22.548456637984177], '清远': [113.06246832527266, 23.688230292088083], '温州': [120.70647689035565, 28.00108540447221], '渭南': [109.51658960525897, 34.50571551675255], '湖州': [120.09451660915789, 30.898963937294184], '湘潭': [112.95046418076468, 27.835702227135585], '湛江': [110.36555441392824, 21.276723439012073], '滁州': [118.33940613596579, 32.26127087204081], '滨州': [117.9774040171467, 37.3881961960769], '漯河': [114.02342077764726, 33.5877107071022], '漳州': [117.65357645298785, 24.51892979117087], '潍坊': [119.16837791142822, 36.71265155126753], '潜江': [112.9054740908161, 30.40835793241892], '潮州': [116.62947017362819, 23.662623192615886], '澄迈': [110.01351091010905, 19.74434867164637], '澳门': [113.55751910182492, 22.204117988443336], '濮阳': [115.03559747034215, 35.76759302890629], '烟台': [121.45441541730195, 37.470038383730525], '焦作': [113.24854783457334, 35.22096325403899], '玉溪': [102.55356029311, 24.35771094244625], '珠海': [113.58255478654918, 22.27656465424921], '白俄罗斯': [], '白银': [104.15541276065119, 36.54146356806949], '百色': [106.62458932565383, 23.908185934295958], '益阳': [112.36151595471031, 28.559711178489888], '盐城': [120.167544265761, 33.355100917626196], '盘锦': [122.07322781023007, 41.14124802295616], '眉山': [103.85656331579456, 30.082526119421058], '石家庄': [114.52153190157445, 38.0483119268727], '福州': [119.30346983854001, 26.080429420698078], '秦皇岛': [119.60853063334328, 39.941748102377936], '简阳': [104.55349406265084, 30.41745149135266], '绍兴': [120.58547847885335, 30.0363693113069], '绵阳': [104.6855618607612, 31.473663048745863], '聊城': [115.99158784830443, 36.46275818769411], '肇庆': [112.47148894063035, 23.052888771125616], '自贡': [104.78444884671711, 29.345584921327575], '舟山': [122.21355631852045, 29.99091168016034], '芜湖': [118.43943137653523, 31.358536655799266], '苏州': [120.59241222959322, 31.303564074441766], '茂名': [110.931542579969, 21.669064031332095], '荆州': [112.19641397381135, 30.358989490775382], '荆门': [112.20639298023002, 31.041732575569622], '莆田': [119.0145209781265, 25.45986545592271], '莱芜': [117.68466691247161, 36.23365413364694], '菏泽': [115.48754503343376, 35.23940742476551], '菲律宾': [], '萍乡': [113.8614964337543, 27.6283927093972], '营口': [122.24157466449694, 40.67313683826707], '蚌埠': [117.39551332813694, 32.921523704350825], '衡水': [115.6754061376161, 37.745191408077424], '衡阳': [112.57844721325992, 26.899576139189122], '衢州': [118.86659674035565, 28.975545802265025], '襄阳': [112.25009284837394, 32.22916859153757], '西双版纳': [100.80344682455637, 22.013601254764165], '西咸新区': [108.710581033887, 34.331138243525466], '西宁': [101.78445017050855, 36.62338469651661], '西安': [125.15537330312809, 42.933308420624584], '西昌': [102.27148382916775, 27.900580896263623], '许昌': [113.85847553685502, 34.04143161161871], '贵阳': [106.63657676352776, 26.653324822309752], '贺州': [111.57352631416218, 24.409450902865487], '资阳': [112.33043548238085, 28.59723454973666], '赣州': [114.9405033729825, 25.835176103497655], '赤峰': [118.8955203975195, 42.2616861034116], '辽阳': [123.24336640651318, 41.27416129045421], '达州': [107.47459385897544, 31.214307723927455], '运城': [111.01338945447925, 35.03270691290923], '连云港': [119.22862133316607, 34.60224952526725], '通化': [125.94660627598029, 41.733815801613424], '通辽': [122.25052178737633, 43.657980083916655], '遂宁': [105.5994215306444, 30.53909767110912], '遵义': [106.93342774801829, 27.731700878916666], '邢台': [114.51146225612979, 37.07668595096609], '邯郸': [114.5456282282352, 36.631262731204046], '邵阳': [111.474432885931, 27.245270272808565], '郑州': [113.63141920733915, 34.75343885045448], '郴州': [113.02146049909462, 25.776683273601865], '鄂尔多斯': [109.78744317923602, 39.61448231394889], '鄂州': [114.90160738827099, 30.39657217331699], '酒泉': [98.50068521606795, 39.73846908071564], '重庆': [106.55843415537664, 29.568996245338923], '金华': [119.65343619052916, 29.084639385513697], '钦州': [108.66058016842224, 21.986593539484296], '铁岭': [123.73236520917769, 42.22994799718447], '铜陵': [117.81847679445747, 30.95123323991339], '银川': [106.23849358740017, 38.492460055509596], '锦州': [121.13259630055518, 41.10093149946208], '镇江': [119.43048944567383, 32.19471592052375], '长春': [125.3306020759069, 43.82195350104314], '长沙': [112.94547319535287, 28.23488939994364], '长治': [113.12255886984902, 36.2012683721548], '阜阳': [115.82043612491321, 32.89606099485221], '防城港': [108.360418838298, 21.6930052899694], '阳江': [111.98848929181268, 21.864339726138933], '阳泉': [113.58761666287546, 37.862360847859385], '阿坝': [102.23141546175019, 31.905511577266523], '随州': [113.38945001822157, 31.6965167723283], '雅安': [103.04954262360451, 30.01679254570607], '青岛': [120.38945519114627, 36.072227496663224], '鞍山': [123.00137251399407, 41.11505359694933], '韶关': [113.60352734562261, 24.815881278583017], '马鞍山': [118.5135795794315, 31.676265597609103], '驻马店': [114.02847078173271, 33.01784241674367], '鹤壁': [114.30359364247649, 35.7523574114], '鹰潭': [117.0755754270272, 28.265787063191418], '黄石': [115.04553290894361, 30.205207848941598], '黔东南': [107.9894462407788, 26.58970296982603], '黔南': [107.5284027057371, 26.260616196073833], '龙岩': [117.02344756677536, 25.081219844871676]}

def predict(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        is_success = model_ceshi(data)
        packet_data = {
            "message": is_success
        }
        return JsonResponse(packet_data, safe=False)
def predict_page(request):
    if request.method == "GET":
        return render(request, "index/predict.html")
def data_to_sql(request):
    if request.method == "GET":
        is_success = run_sql()
        packet_data = {
            "message": "爬虫数据写入数据库成功"
        }
        return JsonResponse(packet_data, safe=False)

def data_init(request):
    if request.method == "GET":
        is_success = run()
        packet_data = {
            "message": "数据初始化成功"
        }
        return JsonResponse(packet_data, safe=False)

def data_init_page(request):
    return render(request, "index/data_init_page.html")

def onlineSpider(request):
    return render(request, "index/onlineSpider.html")

def index(request):
    return render(request, "index/index.html")

def datatable(request):
    return render(request, "index/datatable.html")

def getJobsInfo(request):
    if request.method == "GET":
        city = request.GET.get('city', '')
        job_experience = request.GET.get('job_experience', '')
        education = request.GET.get('education', '')
        post_type = request.GET.get('post_type', '')
        page = request.GET.get('pageNumber', 1)  # 获取当前页码
        limit = request.GET.get('pageSize', 10)  # 获取每页显示的记录数
        base_query = Q()
        if city:
            base_query &= Q(job_area__icontains=city)
        if job_experience:
            base_query &= Q(year__icontains=job_experience)
        if education:
            base_query &= Q(education__icontains=education)
        if post_type:
            base_query &= Q(type=post_type)

        all_jobs = Jobinfo.objects.filter(base_query)
        total = all_jobs.count()  # 计算总记录数

        paginator = Paginator(all_jobs, limit)  # 使用分页器
        jobs_page = paginator.get_page(page)  # 获取当前页的数据

        data = list(jobs_page.object_list.values())  # 将QuerySet转换为字典列表

        packet_data = {
            "total": total,
            "rows": data
        }
        return JsonResponse(packet_data, safe=False)

def avgWageOfCityAndJob(request):
    return render(request, "index/avgWageOfCityAndJob.html")

def getAvgSalaryByCityAndJobType(request):
    category = request.GET.get("category","岗位")
    result = {}
    avawage = getAvgSalaryByCatetory(category)
    avawage = sorted(avawage.items(), key = operator.itemgetter(1), reverse = True)
    if category=="城市":  #返回前100个
        avawage = avawage[:100]
        print(avawage)
    names = []
    avawage_ls = []

    for wage in avawage:
        names.append(wage[0])
        avawage_ls.append(wage[1])
    result["names"] = names
    result["AvgWage"] = avawage_ls
    return HttpResponse(json.dumps(result), content_type="application/json")

def everyJobTypeCountInCity(request):
    return render(request, "index/everyJobTypeCountInCity.html")

def getJobTypeCountByCity(request):
    city = request.GET.get("city","北京")
    jobTypeCountsDic = sorted(getEveryJobTypeCountsByCity(city),key=lambda x:x['count'], reverse=True)[:10]
    result = {}
    names=[]
    counts=[]
    for var in jobTypeCountsDic:
        names.append(var["type"])
        counts.append(var["count"])

    result["names"] = names
    result["counts"] = counts
    return HttpResponse(json.dumps(result), content_type="application/json")


def job_count_inCity(request):
    return render(request, "index/job_count_inCity.html")

def getJobCountsByEveryCity(request):
    re = getJobCountsByCity()
    result = {}
    jobCountOfCity = sorted(re,key=lambda records:records['value'], reverse = True)[:36]
    result["jobCountOfCity"] = jobCountOfCity

    lngAndLatOfCity = {}
    for var in jobCountOfCity:
        lngAndLatOfCity[var["name"]] = ALL_CITIES_LNG_LAT[var["name"]]
    result["lngAndLatOfCity"] = lngAndLatOfCity
    return HttpResponse(json.dumps(result), content_type="application/json")

def educationAndExperienceOfCity(request):
    return render(request, "index/educationAndExperienceOfCity.html")


def getEducationAndExperienceOfCity(request):
    result = {}
    educationName = []
    jobExperienceName = []
    postType = request.GET.get("post_type", "")

    educationDemands = getEducationDemandByJobType(postType)
    jobExperienceDemands = getJobExperienceByJobType(postType)

    for var in educationDemands:
        educationName.append(var["name"])

    for var in jobExperienceDemands:
        jobExperienceName.append(var["name"])

    result["seriesData"] = educationDemands
    result["legendData"] = educationName

    result["seriesData2"] = jobExperienceDemands
    result["legendData2"] = jobExperienceName
    return HttpResponse(json.dumps(result), content_type="application/json")

# 函数
def getAvgSalaryByCatetory(category):
    result = {}
    if category=="岗位":
        allPostTypes = getSingleFiledAndDistinct("type")
        for postType in allPostTypes:
            salaries = Jobinfo.objects.filter(type=postType).values("salary_top","salary_bot")
            sa_num = 0.0
            for salary in salaries:
                sa_num +=float(salary["salary_top"])+float(salary["salary_bot"])
            sa_num /= 2.0*len(salaries)
            result[postType] = round(sa_num,1)

    elif category == "城市":
        allCities = getSingleFiledAndDistinct("job_area")
        for city in allCities:
            salaries = Jobinfo.objects.filter(job_area__icontains=city).values("salary_top", "salary_bot")
            sa_num = 0.0
            for salary in salaries:
                sa_num += float(salary["salary_top"]) + float(salary["salary_bot"])
            sa_num /= 2.0 * len(salaries)
            result[city] = round(sa_num, 1)
    return result

def getSingleFiledAndDistinct(filed):
    return list(Jobinfo.objects.values_list(filed,flat=True).distinct().order_by(filed))

def getEveryJobTypeCountsByCity(city):
    return list(Jobinfo.objects.filter(job_area=city).values("type").annotate(count=Count('type')).values('type','count').order_by("count"))

def getJobCountsByCity():
    return list(Jobinfo.objects.values('job_area').annotate(name=F('job_area'),value=Count('name')).values('name', 'value').order_by())

def getEducationDemandByJobType(JobType):
    return list(Jobinfo.objects.filter(type=JobType).values("education").annotate(name=F('education'),value=Count('name')).values('name', 'value').order_by())

def getJobExperienceByJobType(JobType):
    return list(Jobinfo.objects.filter(type=JobType).values("year").annotate(name=F('year'),value=Count('name')).values('name', 'value').order_by())

