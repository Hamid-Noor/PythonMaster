import streamlit as st

def setup_persian_ui():
    """تنظیم رابط کاربری فارسی"""
    st.markdown("""
    <style>
    .main .block-container {
        direction: rtl;
        text-align: right;
    }
    
    .stSelectbox label {
        direction: rtl;
        text-align: right;
    }
    
    .stTextArea label {
        direction: rtl;
        text-align: right;
    }
    
    .stTextInput label {
        direction: rtl;
        text-align: right;
    }
    
    .stRadio label {
        direction: rtl;
        text-align: right;
    }
    
    .stCheckbox label {
        direction: rtl;
        text-align: right;
    }
    
    .stButton button {
        direction: rtl;
    }
    
    .stExpander {
        direction: rtl;
        text-align: right;
    }
    
    .stAlert {
        direction: rtl;
        text-align: right;
    }
    
    .stInfo {
        direction: rtl;
        text-align: right;
    }
    
    .stSuccess {
        direction: rtl;
        text-align: right;
    }
    
    .stWarning {
        direction: rtl;
        text-align: right;
    }
    
    .stError {
        direction: rtl;
        text-align: right;
    }
    
    .stMetric {
        direction: rtl;
        text-align: right;
    }
    
    .stDataFrame {
        direction: rtl;
    }
    
    .stMarkdown {
        direction: rtl;
        text-align: right;
    }
    
    .stSidebar {
        direction: rtl;
        text-align: right;
    }
    
    .stTab {
        direction: rtl;
        text-align: right;
    }
    
    /* فونت فارسی */
    .stApp {
        font-family: 'Tahoma', 'Arial', sans-serif;
    }
    
    /* تنظیمات کد */
    .stCode {
        direction: ltr;
        text-align: left;
    }
    
    /* تنظیمات جدول */
    .stTable {
        direction: rtl;
    }
    
    /* تنظیمات فرم */
    .stForm {
        direction: rtl;
        text-align: right;
    }
    
    /* تنظیمات نمودار */
    .stPlotlyChart {
        direction: ltr;
    }
    
    .stGraphvizChart {
        direction: ltr;
    }
    
    /* تنظیمات متن */
    h1, h2, h3, h4, h5, h6 {
        direction: rtl;
        text-align: right;
    }
    
    p {
        direction: rtl;
        text-align: right;
    }
    
    ul, ol {
        direction: rtl;
        text-align: right;
    }
    
    /* تنظیمات کلمن‌ها */
    .stColumns {
        direction: rtl;
    }
    
    /* تنظیمات اسپینر */
    .stSpinner {
        direction: rtl;
        text-align: right;
    }
    
    /* تنظیمات پیام‌ها */
    .stToast {
        direction: rtl;
        text-align: right;
    }
    
    /* تنظیمات بارگذاری فایل */
    .stFileUploader {
        direction: rtl;
        text-align: right;
    }
    
    /* تنظیمات تاریخ */
    .stDateInput {
        direction: rtl;
        text-align: right;
    }
    
    /* تنظیمات زمان */
    .stTimeInput {
        direction: rtl;
        text-align: right;
    }
    
    /* تنظیمات اسلایدر */
    .stSlider {
        direction: rtl;
        text-align: right;
    }
    
    /* تنظیمات انتخاب عدد */
    .stNumberInput {
        direction: rtl;
        text-align: right;
    }
    
    /* تنظیمات سلکت باکس چندگانه */
    .stMultiSelect {
        direction: rtl;
        text-align: right;
    }
    
    /* تنظیمات کمرا */
    .stCameraInput {
        direction: rtl;
        text-align: right;
    }
    
    /* تنظیمات رنگ */
    .stColorPicker {
        direction: rtl;
        text-align: right;
    }
    
    /* تنظیمات نقشه */
    .stMap {
        direction: ltr;
    }
    
    /* تنظیمات پیشرفت */
    .stProgress {
        direction: rtl;
        text-align: right;
    }
    
    /* تنظیمات پیام حالت */
    .stStatus {
        direction: rtl;
        text-align: right;
    }
    
    /* تنظیمات دیتافریم */
    .stDataEditor {
        direction: rtl;
    }
    
    /* تنظیمات چت */
    .stChat {
        direction: rtl;
        text-align: right;
    }
    
    /* تنظیمات پیام چت */
    .stChatMessage {
        direction: rtl;
        text-align: right;
    }
    
    /* تنظیمات ورودی چت */
    .stChatInput {
        direction: rtl;
        text-align: right;
    }
    
    /* تنظیمات عنصر */
    .element-container {
        direction: rtl;
        text-align: right;
    }
    
    /* تنظیمات بلاک */
    .block-container {
        direction: rtl;
        text-align: right;
    }
    
    /* تنظیمات ردیف */
    .row-widget {
        direction: rtl;
        text-align: right;
    }
    
    /* تنظیمات کلید */
    .stTabs {
        direction: rtl;
        text-align: right;
    }
    
    /* تنظیمات محتوای تب */
    .stTabContent {
        direction: rtl;
        text-align: right;
    }
    
    /* تنظیمات کانتینر */
    .stContainer {
        direction: rtl;
        text-align: right;
    }
    
    /* تنظیمات پاپ اپ */
    .stPopover {
        direction: rtl;
        text-align: right;
    }
    
    /* تنظیمات مودال */
    .stModal {
        direction: rtl;
        text-align: right;
    }
    
    /* تنظیمات تولتیپ */
    .stTooltip {
        direction: rtl;
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

def get_text(key: str) -> str:
    """دریافت متن فارسی"""
    texts = {
        'title': 'پلتفرم آموزش معکوس برنامه‌نویسی پایتون',
        'welcome': 'خوش آمدید!',
        'code_analysis': 'تحلیل کد',
        'exercises': 'تمرین‌ها',
        'progress': 'پیشرفت',
        'start': 'شروع',
        'next': 'بعدی',
        'previous': 'قبلی',
        'submit': 'ارسال',
        'check_answer': 'بررسی پاسخ',
        'hint': 'راهنمایی',
        'explanation': 'توضیح',
        'correct': 'صحیح',
        'incorrect': 'نادرست',
        'score': 'امتیاز',
        'difficulty': 'سطح دشواری',
        'beginner': 'مبتدی',
        'intermediate': 'متوسط',
        'advanced': 'پیشرفته',
        'variables': 'متغیرها',
        'functions': 'توابع',
        'classes': 'کلاس‌ها',
        'loops': 'حلقه‌ها',
        'conditions': 'شرطی‌ها',
        'imports': 'وابستگی‌ها',
        'error': 'خطا',
        'warning': 'هشدار',
        'info': 'اطلاعات',
        'success': 'موفقیت',
        'loading': 'در حال بارگذاری...',
        'processing': 'در حال پردازش...',
        'completed': 'تکمیل شده',
        'not_completed': 'تکمیل نشده',
        'try_again': 'دوباره تلاش کنید',
        'well_done': 'آفرین!',
        'excellent': 'عالی!',
        'good': 'خوب',
        'needs_improvement': 'نیاز به بهبود',
        'total': 'کل',
        'average': 'میانگین',
        'percentage': 'درصد',
        'questions': 'سوالات',
        'answers': 'پاسخ‌ها',
        'results': 'نتایج',
        'statistics': 'آمار',
        'overview': 'نمای کلی',
        'details': 'جزئیات',
        'settings': 'تنظیمات',
        'help': 'راهنما',
        'about': 'درباره',
        'contact': 'تماس',
        'feedback': 'بازخورد',
        'report': 'گزارش',
        'save': 'ذخیره',
        'load': 'بارگذاری',
        'export': 'خروجی',
        'import': 'ورودی',
        'clear': 'پاک کردن',
        'reset': 'بازنشانی',
        'confirm': 'تایید',
        'cancel': 'لغو',
        'close': 'بستن',
        'open': 'باز کردن',
        'edit': 'ویرایش',
        'delete': 'حذف',
        'add': 'اضافه کردن',
        'remove': 'حذف کردن',
        'update': 'به‌روزرسانی',
        'refresh': 'تازه‌سازی',
        'search': 'جستجو',
        'filter': 'فیلتر',
        'sort': 'مرتب‌سازی',
        'view': 'نمایش',
        'hide': 'پنهان کردن',
        'show': 'نمایش دادن',
        'expand': 'گسترش',
        'collapse': 'جمع کردن',
        'select': 'انتخاب',
        'deselect': 'لغو انتخاب',
        'select_all': 'انتخاب همه',
        'deselect_all': 'لغو انتخاب همه',
        'copy': 'کپی',
        'paste': 'چسباندن',
        'cut': 'برش',
        'undo': 'واگرد',
        'redo': 'تکرار',
        'bold': 'پررنگ',
        'italic': 'کج',
        'underline': 'زیرخط',
        'strikethrough': 'خط خورده',
        'highlight': 'برجسته',
        'color': 'رنگ',
        'size': 'اندازه',
        'font': 'فونت',
        'align': 'تراز',
        'left': 'چپ',
        'right': 'راست',
        'center': 'وسط',
        'justify': 'قاطع',
        'indent': 'تورفتگی',
        'outdent': 'برآمدگی',
        'list': 'فهرست',
        'numbered': 'شماره‌دار',
        'bulleted': 'نشانه‌دار',
        'table': 'جدول',
        'row': 'ردیف',
        'column': 'ستون',
        'cell': 'سلول',
        'header': 'سرتیتر',
        'footer': 'پاورقی',
        'link': 'پیوند',
        'image': 'تصویر',
        'video': 'ویدیو',
        'audio': 'صوت',
        'file': 'فایل',
        'document': 'سند',
        'folder': 'پوشه',
        'directory': 'دایرکتوری',
        'path': 'مسیر',
        'url': 'آدرس',
        'email': 'ایمیل',
        'phone': 'تلفن',
        'address': 'آدرس',
        'name': 'نام',
        'title_field': 'عنوان',
        'description': 'توضیحات',
        'content': 'محتوا',
        'message': 'پیام',
        'comment': 'نظر',
        'review': 'بررسی',
        'rating': 'امتیازدهی',
        'like': 'پسندیدن',
        'dislike': 'نپسندیدن',
        'favorite': 'مورد علاقه',
        'bookmark': 'نشانک',
        'share': 'اشتراک‌گذاری',
        'download': 'دانلود',
        'upload': 'آپلود',
        'print': 'چاپ',
        'preview': 'پیش‌نمایش',
        'fullscreen': 'تمام صفحه',
        'minimize': 'کوچک کردن',
        'maximize': 'بزرگ کردن',
        'restore': 'بازگردانی',
        'zoom_in': 'بزرگ‌نمایی',
        'zoom_out': 'کوچک‌نمایی',
        'fit': 'متناسب',
        'actual_size': 'اندازه واقعی',
        'rotate': 'چرخش',
        'flip': 'برگرداندن',
        'crop': 'برش',
        'resize': 'تغییر اندازه',
        'move': 'جابجایی',
        'drag': 'کشیدن',
        'drop': 'رها کردن',
        'click': 'کلیک',
        'double_click': 'دوبار کلیک',
        'right_click': 'کلیک راست',
        'hover': 'قرار دادن',
        'focus': 'تمرکز',
        'blur': 'تاری',
        'select_text': 'انتخاب متن',
        'keyboard': 'صفحه‌کلید',
        'mouse': 'ماوس',
        'touch': 'لمس',
        'swipe': 'کشیدن انگشت',
        'pinch': 'نیشگون',
        'scroll': 'پیمایش',
        'pan': 'جابجایی',
        'tap': 'ضربه',
        'press': 'فشار',
        'hold': 'نگه داشتن',
        'release': 'رها کردن'
    }
    
    return texts.get(key, key)

def format_persian_number(number):
    """تبدیل اعداد انگلیسی به فارسی"""
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    english_digits = '0123456789'
    
    result = str(number)
    for i, digit in enumerate(english_digits):
        result = result.replace(digit, persian_digits[i])
    
    return result

def format_english_number(number):
    """تبدیل اعداد فارسی به انگلیسی"""
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    english_digits = '0123456789'
    
    result = str(number)
    for i, digit in enumerate(persian_digits):
        result = result.replace(digit, english_digits[i])
    
    return result

def get_difficulty_color(difficulty):
    """دریافت رنگ مناسب برای سطح دشواری"""
    colors = {
        'مبتدی': '#4CAF50',    # سبز
        'متوسط': '#FF9800',    # نارنجی
        'پیشرفته': '#F44336'   # قرمز
    }
    return colors.get(difficulty, '#9E9E9E')

def get_score_color(score):
    """دریافت رنگ مناسب برای امتیاز"""
    if score >= 80:
        return '#4CAF50'  # سبز
    elif score >= 60:
        return '#FF9800'  # نارنجی
    else:
        return '#F44336'  # قرمز

def persian_sort_key(text):
    """کلید مرتب‌سازی فارسی"""
    persian_order = 'اآبپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی'
    result = []
    
    for char in text:
        if char in persian_order:
            result.append(persian_order.index(char))
        else:
            result.append(ord(char))
    
    return result

def truncate_persian_text(text, max_length=50):
    """کوتاه کردن متن فارسی"""
    if len(text) <= max_length:
        return text
    
    truncated = text[:max_length-3]
    # اطمینان از عدم بریده شدن کلمه
    if text[max_length-3] != ' ':
        last_space = truncated.rfind(' ')
        if last_space > 0:
            truncated = truncated[:last_space]
    
    return truncated + '...'

def is_rtl_text(text):
    """تشخیص جهت متن (راست به چپ یا چپ به راست)"""
    rtl_chars = set('ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی')
    
    for char in text:
        if char in rtl_chars:
            return True
    
    return False

def get_text_direction(text):
    """دریافت جهت متن"""
    return 'rtl' if is_rtl_text(text) else 'ltr'

def format_persian_date(date):
    """قالب‌بندی تاریخ فارسی"""
    # این تابع می‌تواند برای تبدیل تاریخ میلادی به شمسی استفاده شود
    # برای سادگی، فقط قالب‌بندی ساده انجام می‌دهیم
    return date.strftime('%Y/%m/%d')

def get_persian_weekday(date):
    """دریافت نام روز هفته فارسی"""
    weekdays = [
        'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنج‌شنبه',
        'جمعه', 'شنبه', 'یکشنبه'
    ]
    return weekdays[date.weekday()]

def get_persian_month(month):
    """دریافت نام ماه فارسی"""
    months = [
        'فروردین', 'اردیبهشت', 'خرداد', 'تیر',
        'مرداد', 'شهریور', 'مهر', 'آبان',
        'آذر', 'دی', 'بهمن', 'اسفند'
    ]
    return months[month - 1] if 1 <= month <= 12 else str(month)

def clean_persian_text(text):
    """پاکسازی متن فارسی"""
    # حذف فاصله‌های اضافی
    text = ' '.join(text.split())
    
    # تبدیل ی عربی به فارسی
    text = text.replace('ي', 'ی')
    
    # تبدیل ک عربی به فارسی
    text = text.replace('ك', 'ک')
    
    # تبدیل اعداد عربی به فارسی
    arabic_digits = '٠١٢٣٤٥٦٧٨٩'
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    
    for i, digit in enumerate(arabic_digits):
        text = text.replace(digit, persian_digits[i])
    
    return text

def validate_persian_input(text):
    """اعتبارسنجی ورودی فارسی"""
    if not text or not text.strip():
        return False, "متن نمی‌تواند خالی باشد"
    
    # بررسی طول متن
    if len(text.strip()) < 2:
        return False, "متن باید حداقل 2 کاراکتر باشد"
    
    # بررسی وجود حداقل یک کاراکتر فارسی
    if not is_rtl_text(text):
        return False, "متن باید شامل کاراکترهای فارسی باشد"
    
    return True, "معتبر"

def highlight_code_keywords(code):
    """برجسته کردن کلیدواژه‌های کد"""
    keywords = [
        'def', 'class', 'if', 'else', 'elif', 'for', 'while',
        'try', 'except', 'finally', 'import', 'from', 'return',
        'break', 'continue', 'pass', 'lambda', 'with', 'as',
        'raise', 'assert', 'del', 'global', 'nonlocal', 'yield',
        'True', 'False', 'None', 'and', 'or', 'not', 'in', 'is'
    ]
    
    highlighted = code
    for keyword in keywords:
        highlighted = highlighted.replace(
            keyword, 
            f'<span style="color: #0066CC; font-weight: bold;">{keyword}</span>'
        )
    
    return highlighted

def get_error_message(error_type, details=""):
    """دریافت پیام خطای فارسی"""
    error_messages = {
        'syntax_error': 'خطای نحوی در کد',
        'runtime_error': 'خطای زمان اجرا',
        'type_error': 'خطای نوع داده',
        'name_error': 'خطای نام متغیر',
        'index_error': 'خطای ایندکس',
        'key_error': 'خطای کلید',
        'value_error': 'خطای مقدار',
        'attribute_error': 'خطای خاصیت',
        'import_error': 'خطای وارد کردن',
        'io_error': 'خطای ورودی/خروجی',
        'network_error': 'خطای شبکه',
        'permission_error': 'خطای مجوز',
        'file_not_found': 'فایل یافت نشد',
        'connection_error': 'خطای اتصال',
        'timeout_error': 'خطای زمان‌بندی',
        'unknown_error': 'خطای نامشخص'
    }
    
    base_message = error_messages.get(error_type, 'خطای نامشخص')
    
    if details:
        return f"{base_message}: {details}"
    else:
        return base_message

def get_success_message(action):
    """دریافت پیام موفقیت فارسی"""
    success_messages = {
        'saved': 'با موفقیت ذخیره شد',
        'loaded': 'با موفقیت بارگذاری شد',
        'updated': 'با موفقیت به‌روزرسانی شد',
        'deleted': 'با موفقیت حذف شد',
        'created': 'با موفقیت ایجاد شد',
        'completed': 'با موفقیت تکمیل شد',
        'submitted': 'با موفقیت ارسال شد',
        'verified': 'با موفقیت تایید شد',
        'exported': 'با موفقیت خروجی گرفته شد',
        'imported': 'با موفقیت وارد شد',
        'connected': 'با موفقیت متصل شد',
        'disconnected': 'با موفقیت قطع شد',
        'reset': 'با موفقیت بازنشانی شد',
        'synchronized': 'با موفقیت همگام‌سازی شد',
        'backup_created': 'نسخه پشتیبان با موفقیت ایجاد شد',
        'restored': 'با موفقیت بازگردانی شد'
    }
    
    return success_messages.get(action, 'عملیات با موفقیت انجام شد')
