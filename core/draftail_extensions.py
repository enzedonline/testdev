from wagtail.admin.rich_text.converters.html_to_contentstate import (
    BlockElementHandler, InlineEntityElementHandler, InlineStyleElementHandler)
from wagtail.admin.rich_text.editors.draftail.features import \
    InlineStyleFeature
from draftjs_exporter.dom import DOM
import wagtail.admin.rich_text.editors.draftail.features as draftail_features


def register_inline_styling(
    features,
    feature_name,
    description,
    type_,
    tag='span',
    format=None,
    editor_style=None,
    label=None,
    icon=None
):
    control = {"type": type_, "description": description}
    if label:
        control["label"] = label
    elif icon:
        control["icon"] = icon
    else:
        control["label"] = description
    if editor_style:
        control["style"] = editor_style

    if not format:
        style_map = {"element": tag}
        markup_map = tag
    else:
        style_map = f'{tag} {format}'
        markup_map = f'{tag}[{format}]'

    features.register_editor_plugin(
        "draftail", feature_name, InlineStyleFeature(control)
    )
    db_conversion = {
        "from_database_format": {markup_map: InlineStyleElementHandler(type_)},
        "to_database_format": {"style_map": {type_: style_map}},
    }
    features.register_converter_rule("contentstate", feature_name, db_conversion)
    
def register_block_feature(
    features,
    feature_name,
    type_,
    description,
    css_class,
    element="div",
    wrapper=None,
    label=None,
    icon=None,
    editor_style=None,
):
    control = {
        "type": type_,
        "description": description,
        "element": element,
    }
    if label:
        control["label"] = label
    elif icon:
        control["icon"] = icon
    else:
        control["label"] = description
    if editor_style:
        control["style"] = editor_style

    features.register_editor_plugin(
        "draftail",
        feature_name,
        draftail_features.BlockFeature(control, css={"all": ["draftail-editor.css"]}),
    )

    block_map = {"element": element, "props": {"class": css_class}}
    if wrapper:
        block_map["wrapper"] = wrapper

    features.register_converter_rule(
        "contentstate",
        feature_name,
        {
            "from_database_format": {
                f"{element}[class={css_class}]": BlockElementHandler(type_)
            },
            "to_database_format": {
                "block_map": {
                    type_: block_map
                }
            },
        },
    )

    
#--------------------------------------------------------------------------------------------------    
# SVG icons
#--------------------------------------------------------------------------------------------------  
class DRAFTAIL_ICONS:
    left_align = [
        "M 584.19821,168.76226 H 73.024776 C 32.701407,168.76226 0,137.69252 0,99.38113 0,\
        61.069736 32.701407,30 73.024776,30 H 584.19821 c 40.39183,0 73.02477,31.069736 73.02477,\
        69.38113 0,38.31139 -32.63294,69.38113 -73.02477,69.38113 z m 0,\
        555.04902 H 73.024776 C 32.701407,723.81128 0,692.80659 0,654.43015 0,616.05372 32.701407,\
        585.04902 73.024776,585.04902 H 584.19821 c 40.39183,0 73.02477,31.0047 73.02477,69.38113 0,\
        38.37644 -32.63294,69.38113 -73.02477,69.38113 z M 0,376.90564 C 0,338.5292 32.701407,\
        307.52451 73.024776,307.52451 H 949.32209 c 40.39183,0 73.02481,31.00469 73.02481,69.38113 0,\
        38.37644 -32.63298,69.38113 -73.02481,69.38113 H 73.024776 C 32.701407,446.28677 0,415.28208 0,\
        376.90564 Z M 949.32209,1001.3358 H 73.024776 C 32.701407,1001.3358 0,970.3311 0,931.95467 0,\
        893.57823 32.701407,862.57354 73.024776,862.57354 H 949.32209 c 40.39183,0 73.02481,\
        31.00469 73.02481,69.38113 0,38.37643 -32.63298,69.38113 -73.02481,69.38113 z"
    ]

    centre_align = [
        "M 729.54876,161.46125 H 293.0195 c -40.24254,0 -72.75487,-31.67405 -72.75487,-70.73062 C 220.26463,\
        51.674059 252.77696,20 293.0195,20 h 436.52926 c 40.24254,0 72.75488,31.674059 72.75488,70.73063 0,\
        39.05657 -32.51234,70.73062 -72.75488,70.73062 z M 947.81339,444.38376 H 74.754876 C 34.580543,\
        444.38376 2,412.77601 2,373.65314 2,334.53026 34.580543,302.92251 74.754876,\
        302.92251 H 947.81339 c 40.24254,0 72.75491,31.60775 72.75491,70.73063 0,39.12287 -32.51237,\
        70.73062 -72.75491,70.73062 z M 2,939.49815 C 2,900.37528 34.580543,868.76753 74.754876,\
        868.76753 H 947.81339 c 40.24254,0 72.75491,31.60775 72.75491,70.73062 0,39.12288 -32.51237,\
        70.73065 -72.75491,70.73065 H 74.754876 C 34.580543,1010.2288 2,978.62103 2,939.49815 Z M 729.54876,\
        727.30627 H 293.0195 c -40.24254,0 -72.75487,-31.60775 -72.75487,-70.73062 0,-39.12288 32.51233,\
        -70.73063 72.75487,-70.73063 h 436.52926 c 40.24254,0 72.75488,31.60775 72.75488,70.73063 0,\
        39.12287 -32.51234,70.73062 -72.75488,70.73062 z"
    ]

    right_align = [
        "M 947.56774,163.47496 H 437.33896 c -40.31719,0 -72.88983,-29.43806 -72.88983,\
        -65.73748 C 364.44913,61.438065 397.02177,32 437.33896,32 h 510.22878 c 40.31718,\
        0 72.88986,29.438065 72.88986,65.73748 0,36.29942 -32.57268,65.73748 -72.88986,\
        65.73748 z m 0,525.89984 H 437.33896 c -40.31719,0 -72.88983,-29.37643 -72.88983,\
        -65.73748 0,-36.36104 32.57264,-65.73748 72.88983,-65.73748 h 510.22878 c 40.31718,\
        0 72.88986,29.37644 72.88986,65.73748 0,36.36105 -32.57268,65.73748 -72.88986,65.73748 z M 0,\
        360.6874 C 0,324.32636 32.640975,294.94992 72.889826,294.94992 H 947.56774 c 40.31718,\
        0 72.88986,29.37644 72.88986,65.73748 0,36.36104 -32.57268,65.73748 -72.88986,\
        65.73748 H 72.889826 C 32.640975,426.42488 0,397.04844 0,360.6874 Z M 947.56774,\
        952.32472 H 72.889826 C 32.640975,952.32472 0,922.94829 0,886.58724 0,850.2262 32.640975,\
        820.84976 72.889826,820.84976 H 947.56774 c 40.31718,0 72.88986,29.37644 72.88986,65.73748 0,\
        36.36105 -32.57268,65.73748 -72.88986,65.73748 z"
    ]
    
    underline = [
        "m 38.444913,116.09067 c 0,-38.152504 32.572641,-68.976279 72.889827,-68.976279 h 218.66948 c 40.31718,\
        0 72.88982,30.823775 72.88982,68.976279 0,38.15251 -32.57264,68.97628 -72.88982,\
        68.97628 H 293.5593 v 275.90512 c 0,114.24194 97.94571,206.92882 218.66948,206.92882 120.72378,\
        0 218.66948,-92.68688 218.66948,-206.92882 V 185.06695 h -36.44491 c -40.31719,0 -72.88983,\
        -30.82377 -72.88983,-68.97628 0,-38.152504 32.57264,-68.976279 72.88983,-68.976279 h 218.66948 c 40.31718,\
        0 72.88982,30.823775 72.88982,68.976279 0,38.15251 -32.57264,68.97628 -72.88982,\
        68.97628 h -36.44492 v 275.90512 c 0,190.54696 -163.09098,344.88138 -364.44913,344.88138 -201.35814,\
        0 -364.44913,-154.33442 -364.44913,-344.88138 V 185.06695 h -36.44491 c -40.317186,0 -72.889827,\
        -30.82377 -72.889827,-68.97628 z M 2,943.80601 C 2,905.6535 34.572641,874.82973 74.889826,\
        874.82973 H 949.56774 c 40.31718,0 72.88986,30.82377 72.88986,68.97628 0,38.1525 -32.57268,\
        68.97629 -72.88986,68.97629 H 74.889826 C 34.572641,1012.7823 2,981.95851 2,943.80601 Z"
    ]

    font_awesome = [
        "M 1011.0111,38.377438 V 802.30364 c -142.37657,51.24671 -185.81845,72.75487 -269.67821,\
        72.75487 -141.76722,0 -195.43205,-72.75487 -336.92846,-72.75487 -48.94828,0 -86.83863,\
        8.61918 -121.2762,19.93029 -34.66323,10.76317 -66.483,-15.15575 -66.483,-47.89545 v -1.69632 c 0,\
        -21.08755 12.94004,-40.01519 32.54192,-47.42709 42.15555,-16.58334 89.77237,-32.04375 155.21728,\
        -32.04375 141.56412,0 195.22894,72.75488 336.92846,72.75488 57.54639,0 96.7005,-10.46761 161.28786,\
        -33.42177 V 186.84286 c -46.87209,16.5972 -95.3916,33.42177 -161.28786,33.42177 -0.009,0 0.009,0 0,\
        0 -141.74465,0 -195.45461,-72.75488 -336.92846,-72.75488 -128.85878,0 -181.44038,59.3407 -296.08182,\
        68.43506 v 750.0573 c 0,30.23874 -24.259748,54.56619 -54.161303,54.56619 C 24.259752,1020.5683 0,\
        996.24085 0,966.00211 V 56.566157 C 0,26.418355 24.259752,2 54.161307,2 84.062862,2 108.32261,\
        26.418355 108.32261,56.566157 V 108.83599 C 222.96405,97.809077 275.54565,38.377438 404.40443,\
        38.377438 c 141.65438,0 195.09354,72.754872 336.92846,72.754872 84.85272,0 131.56685,\
        -23.076933 269.67821,-72.754872 z"
    ]
    
    decrease_font = [
        "m 69.321184,1023.9321 c -3.246191,-0.2568 -8.463758,-0.9914 -11.372242,-1.6012 -4.252165,\
        -0.8916 -11.697404,-3.2628 -15.752689,-5.0172 C 21.597637,1008.4025 6.4800537,990.82981 1.5848171,\
        970.10678 0.38696444,965.03596 0.00598588,961.63221 5.7485382e-5,955.94876 -0.00947029,\
        946.88252 1.1637954,940.89632 4.6937553,931.99921 6.1960467,928.21272 283.20454,318.50196 286.10456,\
        312.5987 c 3.09676,-6.30368 7.746,-12.77982 12.80945,-17.84281 11.38172,-11.38067 26.4844,\
        -18.62913 43.93361,-21.08566 2.5224,-0.35512 5.10003,-0.46679 10.85108,-0.4701 6.58917,-0.004 8.06147,\
        0.0742 11.64505,0.61713 12.88772,1.95238 23.79741,6.19984 33.74419,13.13759 8.74832,6.10181 16.06293,\
        14.48535 21.31945,24.435 2.48548,4.70456 281.40551,618.22552 282.98477,622.46181 2.72528,7.31062 3.89273,\
        13.93043 3.89273,22.07312 0,13.92377 -4.54279,27.22135 -13.25112,38.78851 -11.82955,15.71311 -30.15897,\
        25.95581 -51.45833,28.75561 -4.68756,0.6162 -14.57365,0.6141 -19.3202,0 -6.55855,-0.8543 -12.49245,\
        -2.3078 -18.65856,-4.5705 -6.45961,-2.3705 -15.52008,-7.5306 -21.05351,-11.9905 -4.93917,-3.9808 -11.43153,\
        -11.21427 -14.73783,-16.42006 -2.45528,-3.86585 -8.02646,-15.8921 -42.01877,-90.70396 L 490.20271,\
        819.2643 H 353.59739 216.99212 l -37.15037,81.83866 c -20.43271,45.01126 -37.79104,83.05109 -38.57409,\
        84.53295 -10.84662,20.52629 -32.04854,34.55579 -57.125498,37.80029 -3.099755,0.401 -12.17943,0.7048 -14.820978,\
        0.4959 z M 427.9861,682.35056 c -0.4264,-1.11107 -74.10889,-163.08491 -74.26366,-163.25141 -0.10243,\
        -0.11017 -16.4299,35.55614 -36.28329,79.25846 -19.85342,43.70234 -36.60565,80.56033 -37.2272,\
        81.90667 l -1.13013,2.44788 h 74.52152 c 62.89412,0 74.4999,-0.0564 74.38276,-0.3616 z M 796.21076,\
        204.35641 c -5.53262,-0.48423 -12.28149,-1.96942 -16.71039,-3.6774 -1.36263,-0.52548 -4.26394,\
        -1.88486 -6.44739,-3.02086 C 769.54369,195.83236 605.5032,96.110098 599.84839,92.36491 584.59662,\
        82.263685 575.78729,64.711048 577.28636,47.409974 579.26832,24.535579 596.88932,6.0058706 621.27028,\
        1.1578021 c 13.1419,-2.6132215 26.64518,-0.77414386 38.37575,5.226582 2.25623,1.1541652 8.80657,\
        4.9612089 14.55632,8.4600969 5.74974,3.498889 12.89557,7.847029 15.87962,9.662534 2.98404,1.815506 6.7356,\
        4.102759 8.3368,5.082786 1.60119,0.980026 7.02011,4.281182 12.04204,7.335903 5.02193,3.054722 13.00144,\
        7.91127 17.73224,10.792333 4.73081,2.881062 11.87663,7.228358 15.87962,9.660658 15.88415,9.651535 20.12787,\
        12.233323 37.84423,23.023509 10.11545,6.160827 18.51339,11.201504 18.6621,11.201504 0.14871,0 31.036,\
        -18.725374 68.63838,-41.611941 37.60241,-22.886567 69.42231,-42.1847448 70.71089,-42.8848357 24.1081,\
        -13.0979256 55.47598,-7.54701418 72.47083,12.8245467 12.7071,15.231862 15.18,35.595221 6.404,\
        52.735074 -3.9737,7.760993 -8.9518,13.495561 -16.2036,18.666005 -3.67103,2.617413 -169.84937,\
        104.002823 -174.49718,106.460743 -5.44713,2.88062 -12.53875,5.14997 -18.92593,6.05637 -2.95697,\
        0.41961 -10.56408,0.71692 -12.96563,0.50674 z"
    ]
    
    highlighter = ["m 592.83219,630.12307 298.10994,-430.084 -55.14282,-58.81149 -404.8197,316.8619 z \
        m -351.9353,10.00197 v 0 V 496.697 c 0,-30.60597 13.55045,-59.21155 36.69913,\
        -77.21507 L 791.57214,16.803282 C 805.49899,5.801133 822.43706,0 839.75152,0 861.2064,\
        0 881.90848,9.0017582 897.15274,25.204923 L 1000.2867,134.82633 C 1015.531,151.0295 1024,\
        172.83376 1024,195.83825 c 0,18.40359 -5.4578,36.40711 -15.8089,51.21 L 629.34313,\
        793.1549 c -16.93807,24.60482 -44.03897,39.00763 -72.64545,39.00763 H 421.56957 l -47.80299,\
        50.80992 c -23.52508,25.0049 -61.72983,25.0049 -85.25491,0 L 193.09392,781.55266 c -23.52509,\
        -25.0049 -23.52509,-65.61283 0,-90.6177 z M 13.174049,932.7822 131.74049,806.75758 264.61019,\
        947.98516 206.26797,1009.9973 C 197.79893,1018.999 186.31869,1024 174.27385,\
        1024 H 45.168169 C 20.137475,1024 0,1002.5958 0,975.99061 v -9.40181 c 0,-12.8025 4.7050174,\
        -25.00489 13.174049,-34.00665 z"
    ]

    code_block = [
        "m 449.2,515.6 c -15.624,-15.624 -40.94,-15.624 -56.56,0 l -96,96 c -15.624,\
        15.624 -15.624,41 0,56.62 l 96,96 C 400.6,772.2 410.8,776 421,776 c 10.2,0 20.46,\
        -3.876 28.28,-11.688 15.624,-15.624 15.624,-41 0,-56.62 L 381.6,640 449.32,572.32 C 463.2,\
        556.6 463.2,531.4 449.2,515.6 Z M 855.6,186.76 706.34,37.48 C 682.2,13.484 649.6,0 615.8,\
        0 H 253 C 182.3,0 125,57.3 125,128 l 0.013,768 c 0,70.68 57.3,128 128,128 H 765 c 70.4,\
        0 128,-57.6 128,-128 V 277.2 c 0,-33.8 -13.4,-66.4 -37.4,-90.44 z M 797,896 c 0,\
        17.672 -14.328,32 -32,32 H 253.04 c -17.676,0 -32,-14.328 -32,-32 L 221,128.26 c 0,\
        -17.672 14.328,-32 32,-32 H 573 V 256 c 0,35.34 28.66,64 64,64 H 795.2 V 896 Z M 568.8,\
        515.6 c -15.624,15.624 -15.624,41 0,56.62 l 67.6,67.78 -67.72,67.68 c -15.624,\
        15.624 -15.624,41 0,56.62 7.92,7.9 18.12,11.7 28.32,11.7 10.2,0 20.46,-3.876 28.28,\
        -11.688 l 96,-96 c 15.624,-15.624 15.624,-41 0,-56.62 l -96,-96 C 609.6,500 584.4,\
        500 568.8,515.6 Z"
    ]