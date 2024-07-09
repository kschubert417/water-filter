import os
import time

from flask import request, render_template, Flask

if os.getenv('COMPUTERNAME') == 'DESKTOP-3U5BV0O':
    print("IN TESTING MODE ===================================")
    print("Test CC Number: 4242 4242 4242 4242 with any future date and any 3 digit CVC")
    mode = 'test'
    pmtlink = {'Samsung': 'https://buy.stripe.com/test_aEU02hevSa5A2TCcMM'
               , 'LG': 'https://buy.stripe.com/5kA14P5jp31X608fYZ'}
else:
    mode = 'prod'
    pmtlink = {'Samsung': 'https://buy.stripe.com/5kA14P5jp31X608fYZ'
           , 'LG': 'https://buy.stripe.com/28o9Bl27dfOJ4W4bIK'}


# Dictionary for product details
products = {'Samsung': {'name':'Samsung compatible refrigerator filter', # 'Samsung Compatible Water Filter'
                        'shortdesc':'Compatible with Samsung DA29-00020B refrigerator models', # 'Compatible with most Samsung refrigerators'
                        'longdesc':['Compatible with Samsung DA29-00020B refrigerator models. See below for a complete list of refrigerator models'                                    
                                    , 'The A Better Filter DA29-00020B refrigerator filter provides cleaner, safer quality water as it removes harmful contaminants such as sediment, cyst and lead.'
                                    , 'Tested and certified by WQA against NSF/ANSI 42 for the reduction of chlorine taste and odor as verified and substantiated by test data, and NSF/ANSI 372 for low lead compliance.'],
                        'keyfeatures':['Meets NSF 42 and 53 Certifications'
                                       , 'Reduces chlorine taste and odor'
                                       , 'Reduces sediment, cyst, and lead'], # Max at 3
                        'image':'Samsung_Fridge_Filter.jpg',
                        'pmtlink': pmtlink['Samsung'],
                        'compatible':['RF22K9381SG/AA', 'RF22K9381SR/AA', 'RF22K9581SG/AA', 'RF22K9581SR/AA', 'RF22KREDBSG/AA', 'RF22KREDBSR/AA', 'RF22M9581SG/AA', 'RF22M9581SR/AA', 'RF23HCEDBBC/AA', 'RF23HCEDBSR/AA', 'RF23HCEDBWW/AA', 'RF23HCEDTSR/AA', 'RF23HSESBSR/AA', 'RF23HTEDBSR/AA', 'RF23J9011SG/AA', 'RF23J9011SR/AA', 'RF24FSEDBSR/AA', 'RF24J9960S4/AA'
                                    , 'RF25HMEDBBC/AA', 'RF25HMEDBSG/AA', 'RF25HMEDBSR/AA', 'RF25HMEDBWW/AA', 'RF260BEAEBC/AA', 'RF260BEAESG/AA', 'RF260BEAESP/AA', 'RF260BEAESR/AA', 'RF260BEAEWW/AA', 'RF261BEAEBC/AA', 'RF261BEAESG/AA', 'RF261BEAESP/AA', 'RF261BEAESR/AA', 'RF261BEAEWW/AA', 'RF263BEAEBC/AA', 'RF263BEAESG/AA', 'RF263BEAESP/AA', 'RF263BEAESR/AA'
                                    , 'RF263BEAEWW/AA', 'RF263TEAEBC/AA', 'RF263TEAESG/AA', 'RF263TEAESP/AA', 'RF263TEAESR/AA', 'RF263TEAEWW/AA', 'RF265BEAESG/AA', 'RF265BEAESR/AA', 'RF26HFENDSR/AA', 'RF26J7500BC/AA', 'RF26J7500SR/AA', 'RF26J7500WW/AA', 'RF28HDEDBSR/AA', 'RF28HDEDPBC/AA', 'RF28HDEDPWW/AA', 'RF28HDEDTSR/AA', 'RF28HFEDBBC/AA', 'RF28HFEDBSG/AA'
                                    , 'RF28HFEDBSR/AA', 'RF28HFEDBWW/AA', 'RF28HFEDTBC/AA', 'RF28HFEDTSG/AA', 'RF28HFEDTSR/AA', 'RF28HMEDBBC/AA', 'RF28HMEDBSR/AA', 'RF28HMEDBWW/AA', 'RF28HMELBSR/AA', 'RF28JBEDBSG/AA', 'RF28JBEDBSR/AA', 'RF28K9070SG/AA', 'RF28K9070SR/AA', 'RF28K9380SG/AA', 'RF28K9380SR/AA', 'RF28K9580SG/AA', 'RF28K9580SR/AA', 'RF28M9580SG/AA'
                                    , 'RF28M9580SR/AA', 'RF30HBEDBSR/AA', 'RF30HDEDTSR/AA', 'RF30KMEDBSG/AA', 'RF30KMEDBSR/AA', 'RF31FMEDBBC/AA', 'RF31FMEDBSR/AA', 'RF31FMEDBWW/AA', 'RF31FMESBSR/AA', 'RF323TEDBBC/AA', 'RF323TEDBSR/AA', 'RF323TEDBWW/AA', 'RF32FMQDBSR/AA', 'RF32FMQDBXW/AA', 'RF34H9950S4/AA', 'RF34H9960S4/AA', 'RH22H9010SG/AA', 'RH22H9010SR/AA'
                                    , 'RH25H5611BC/AA', 'RH25H5611SG/AA', 'RH25H5611SR/AA', 'RH25H5611WW/AA', 'RH29H8000SR/AA', 'RH29H9000SR/AA', 'RH30H9500SR/AA', 'RS25H5000BC/AA', 'RS25H5000SR/AA', 'RS25H5000WW/AA', 'RS25H5111BC/AA', 'RS25H5111SG/AA', 'RS25H5111SR/AA', 'RS25H5111WW/AA', 'RS25H5121BC/AA', 'RS25H5121SR/AA', 'RS25H5121WW/AA', 'RS25J500DBC/AA'
                                    , 'RS25J500DSG/AA', 'RS25J500DSR/AA', 'RS25J500DWW/AARS22HDHPNBC/AA', 'RS22HDHPNSR/AA', 'RS22HDHPNWW/AA', 'RS27FDBTNSR/AA', 'RB195BSSB/AA', 'RF263AEBP/AA', 'RF263AEPN/AA', 'RF263AERS/AA', 'RF263AEWP/AA', 'RF263AFBP/AA', 'RF263AFRS/AA', 'RF263AFWP/AA', 'RF265AABP/AA', 'RF265AARS/AA', 'RF265AASH/AA', 'RF265AAWP/AA'
                                    , 'RF265ABBP/AA', 'RF265ABPN/AA', 'RF265ABRS/AA', 'RF265ABWP/AA', 'RF266AABP/AA', 'RF266AARS/AA', 'RF266AASH/AA', 'RF266AAWP/AA', 'RF266ABBP/AA', 'RF266ABPN/AA', 'RF266ABRS/AA', 'RF266ABWP/AA', 'RF266AEBP/AA', 'RF266AEPN/AA', 'RF266AERS/AA', 'RF266AEWP/AA', 'RF266AFRS/AA', 'RF267AABP/AA', 'RF267AARS/AA', 'RF267AASH/AA'
                                    , 'RF267AAWP/AA', 'RF267ABBP/AA', 'RF267ABPN/AA', 'RF267ABRS/AA', 'RF267ABWP/AA', 'RF267AEBP/AA', 'RF267AEPN/AA', 'RF267AERS/AA', 'RF267AEWP/AA', 'RF267AFBP/AA', 'RF267AFRS/AA', 'RF267AFWP/AA', 'RF267HERS/AA', 'RF268ABBP/AA', 'RF268ABPN/AA', 'RF268ABRS/AA', 'RF268ABWP/AA', 'RF26DEPN/AA', 'RF26VABBP/AA', 'RF26VABPN/AA'
                                    , 'RF26VABWP/AA', 'RF26XAEBP/AA', 'RF26XAEPN/AA', 'RF26XAERS/AA', 'RF26XAEWP/AA', 'RF28HDEDPBC/AA', 'RFG237AABP/AA', 'RFG237AAPN/AA', 'RFG237AARS/AA', 'RFG237AAWP/AA', 'RFG237ACRS/AA', 'RFG238AABP/AA', 'RFG238AAPN/AA', 'RFG238AARS/AA', 'RFG238AAWP/AA', 'RFG295AABP/AA', 'RFG295AAPN/AA', 'RFG295AARS/AA'
                                    , 'RFG295AAWP/AA', 'RFG297AABP/AA', 'RFG297AAPN/AA', 'RFG297AARS/AA', 'RFG297AAWP/AA', 'RFG297ACBP/AA', 'RFG297ACRS/AA', 'RFG297ACWP/AA', 'RFG298AABP/AA', 'RFG298AAPN/AA', 'RFG298AARS/AA', 'RFG298AAWP/AA', 'RFG299AARS/AA', 'RH269LBSH/AA', 'RM257ABBP/AA', 'RM257ABRS/AA', 'RM257ACPN/AA', 'RM257ACRS/AA', 'RS21HKLBG/AA'
                                    , 'RS21HKLMR/AA', 'RS22HDHPNBC/AA', 'RS22HDHPNSR/AA', 'RS22HDHPNWW/AA', 'RS2520SW/AA', 'RS2530BBP/AA', 'RS2530BSH/AA', 'RS2530BWP/AA', 'RS2531SW/AA', 'RS2533SW/AA', 'RS2533VQ/AA', 'RS2534BB/AA', 'RS2534VQ/AA', 'RS2534WW/AA', 'RS253BABB/AA', 'RS253BASB/AA', 'RS253BAVQ/AA', 'RS253BAWW/AA', 'RS2542SH/AA', 'RS2544SL/AA'
                                    , 'RS2545SH/AA', 'RS2555BB/AA', 'RS2555SL/AA', 'RS2555SW/AA', 'RS2556BB/AA', 'RS2556SH/AA', 'RS2556WW/AA', 'RS255BABB/AA', 'RS255BASB/AA', 'RS2577BB/AA', 'RS2577SL/AA', 'RS2577SW/AA', 'RS2578BB/AA', 'RS2578SH/AA', 'RS2578WW/AA', 'RS257BARB/AA', 'RS2622SW/AA', 'RS2623SL/AA', 'RS2623VQ/AA', 'RS2623WW/AA'
                                    , 'RS2630ASH/AA', 'RS2630AWW/AA', 'RS2630SH/AA', 'RS2630WW/AA', 'RS263BBSH/AA', 'RS263BBWP/AA', 'RS2644SL/AA', 'RS264ABBP/AA', 'RS264ABRS/AA', 'RS264ABSH/AA', 'RS264ABWP/AA', 'RS265BBWP/AA', 'RS265LABP/AA', 'RS265LBBP/AA', 'RS265LBWP/AA', 'RS2666SW/AA', 'RS267BBBB/AA', 'RS267BBRS/AA', 'RS267BBSH/AA', 'RS267BBWP/AA'
                                    , 'RS267LABB/AA', 'RS267LABP/AA', 'RS267LARS/AA', 'RS267LASH/AA', 'RS267LAWP/AA', 'RS267LAWW/AA', 'RS267LBBP/AA', 'RS267LBRS/AA', 'RS267LBSH/AA', 'RS269LARS/AA', 'RS26XUSW/AA', 'RS275ACBP/AA', 'RS275ACPN/AA', 'RS275ACRS/AA', 'RS275ACWP/AA', 'RS2777SL/AA', 'RS277ACBP/AA', 'RS277ACPN/AA', 'RS277ACRS/AA', 'RS277ACWP/AA'
                                    , 'RS27FDBTNSR/AA', 'RS27KGRS/AA', 'RSC6FWRS/AA', 'RSC6FWSH/AA', 'RSC6JWSH/AA', 'RSC6JWWP/AA', 'RSC6KWRS/AA', 'RSG257AABP/AA', 'RSG257AAPN/AA', 'RSG257AARS/AA', 'RSG257AAWP/AA', 'RSG5FURS/AA', 'SRT768VFHW/AA', 'TS48WLUS/AARF23M8070SG/AA', 'RF23M8070SR/AA', 'RF23M8090SG/AA', 'RF23M8090SR/AA', 'RF23M8570SG/AA'
                                    , 'RF23M8570SR/AA', 'RF23M8590SG/AA', 'RF23M8590SR/AA', 'BRF365200AP/AA', 'BRF425200AP/AA', 'RF23M8960S4/AA', 'RF23M8960MT/AA']},
            'LG': {'name':'LG & Kenmore compatible water filter',
                   'shortdesc':'Compatible with LG LT700P and Kenmore 46-9690 refrigerator models.', # 'Compatible with most LG refrigerators'
                   'longdesc':['Compatible with LG LT700P and Kenmore 46-9690 refrigerator models. See below for a complete list of models'
                               , 'This new filter is much more affordable, while still maintaining the utmost quality standards of drinking water. The NP-LT700P surpasses reduction standards set forth by NSF International for toxins and harmful chemicals. The activated carbon core captures microscopic impurities via adsorption, sequestering chlorine, solid particles including dirt and rust, asbestos, and parasites. Furthermore, the carbon is made out of charred coconut shell, which is a much more natural and environmentally-friendly alternative to coal.'
                               , 'Tested and certified by WQA against NSF/ANSI 42 for the reduction of chlorine taste and odor as verified and substantiated by test data, and NSF/ANSI 372 for low lead compliance.'],
                   'keyfeatures':['Surpasses reduction standards set forth by NSF'
                                  , 'Detoxifies Tap Water via advanced two-stage filtration'
                                  , 'Tested against international standards for the reduction of chlorine, asbestos and parasites'], # Max at 3
                   'image':'LG_Fridge_Filter.jpg',
                   'pmtlink': pmtlink['LG'],
                   'compatible':['LFCS31626S', 'LFD20786SB', 'LFD20786ST', 'LFD20786SW', 'LFD22786SB', 'LFD22786ST', 'LFD22786SW', 'LFX21976ST', 'LFX25976SB', 'LFX25976ST', 'LFX25976SW', 'LFX25978SB', 'LFX25978ST', 'LFX25978SW', 'LFX25991ST', 'LFX25992ST', 'LFX28968D', 'LFX28968SB', 'LFX28968ST', 'LFX28968SW', 'LFX28978SB', 'LFX28978ST', 'LFX28978SW'
                                 , 'LFX28979SB', 'LFX28979ST', 'LFX28979SW', 'LFX28991ST', 'LFX28992ST', 'LFX28995ST', 'LFX29927SB', 'LFX29927ST', 'LFX29927SW', 'LFX29927WB', 'LFX29937ST', 'LFX29945ST', 'LFX31915SB', 'LFX31915ST', 'LFX31915SW', 'LFX31925SB', 'LFX31925ST', 'LFX31925SW', 'LFX31935ST', 'LFX31945ST', 'LFX31995ST', 'LFX32945ST', 'LFX33975ST'
                                 , 'LFXC24726D', 'LFXC24726S', 'LFXC24766*', 'LFXC24766S', 'LFXS24623B', 'LFXS24623D', 'LFXS24623S', 'LFXS24623W', 'LFXS24663S', 'LFXS27566S', 'LFXS29626B', 'LFXS29626S', 'LFXS29626W', 'LFXS29766S', 'LFXS30726B', 'LFXS30726S', 'LFXS30726W', 'LFXS30766D', 'LFXS30766S', 'LFXS30786S', 'LFXS32726S', 'LFXS32736D', 'LFXS32766S'
                                 , 'LFX25991', 'LFX31925ST08', 'LFX31935', 'LFX329345ST', 'LFX33974ST', 'LMX25986ST', 'LMX25986SW', 'LMX25988SB', 'LMX25988ST', 'LMX25988SW', 'LMX28988SB', 'LMX28988ST', 'LMX28988SW', 'LMX28994ST', 'LMX30995ST', 'LMX31985ST', 'LMXC24746S', 'LMXS30746S', 'LMXS30756S', 'LMXS30776S', 'LSXS22423B', 'LSXS22423S', 'LSXS22423W'
                                 , 'LSXS26326B', 'LSXS26326S', 'LSXS26326W', 'LSXS26366S', 'LSXS26386S', 'LSXS27466', 'GF-5D712SL', 'LMX25986SB', 'LSC22991ST', 'LSSB2791ST', 'LSXS26466S', 'ADQ36006101', 'ADQ36006101-S', 'ADQ36006101S', 'ADQ36006102', 'ADQ36006102-S', 'ADQ36006102S', 'LFX25978ST', 'LFX25991ST', 'LFX28978ST', 'LFX31925', 'LFX31925ST'
                                 , 'LFX31925SW', 'LFX31945ST', 'LFX33975ST', 'LGEADQ36006101', 'LMX31985ST', 'LP-1400P', 'LT700P', 'NVW-145', 'PD00001835']}}

# app_log = prebuilt_loggers.filesize_logger('logs/app.log')
# create Flask app instance
app = Flask(__name__, static_url_path='')
application = app

app.secret_key = 'xfdgbsbW$^%W%Hwe57hE56yw56h'

@app.route('/', methods=['GET'])
def index():
    return render_template('home.html', products=products)

@app.route('/aboutus', methods=['GET'])
def aboutus():
    return render_template('about_us.html', products=products)

@app.route('/productinfo', methods=['GET'])
def productinfo():
    product = request.args.get("product", default=None)
    return render_template('productinfo.html', prodname=product, product=products[product], products=products)


if __name__ == '__main__':
    if mode == 'test':
        app.run(host="0.0.0.0", debug=True)
    else:
        app.run(host='0.0.0.0', port=80)
