# encoding: utf-8

import os
import time
from common import read_config
from common.util import *
from common.op_mysql import OpMysql
from common.op_redis import OpRedis

# 读取 .env 配置
TEST_ENV = os.environ['environment']
# 获取测试域名hosts
TIGER_API_HOST = os.environ['tiger_api_host']
PLATFORM_TIGER_API_HOST = os.environ['platform_tiger_api_host']
INTERNAL_ACCOUNT_API_HOST = os.environ['internal_account_api_host']
INTERNAL_ACCOUNT_SERVICE_HOST = os.environ['internal_account_service_host']
EZBUY_API_HOST = os.environ['ezbuy_api_host']
TRANSACTION_ADMIN_API_HOST = os.environ['transaction_admin_api_host']
ORDER_SERVICE_HOST = os.environ['order_service_host']
PRODUCT_SERVICE_HOST = os.environ['product_service_host']
SHIPPING_SERVICE_HOST = os.environ['shipping_service_host']
PAYMENT_SERVICE_HOST = os.environ['payment_service_host']
DINGTALK_SERVICE_HOST = os.environ['dingtalk_service_host']
REAG_DISCOVERY_CENTER_HOST = os.environ['read_discovery_center_host']
REAG_DISCOVERY_CENTER_TOKEN = os.environ['read_discovery_center_token']


#获取内部账号服务ip地址
def get_internal_account_service_host():
    return get_request_host_url(REAG_DISCOVERY_CENTER_HOST,INTERNAL_ACCOUNT_SERVICE_HOST,REAG_DISCOVERY_CENTER_TOKEN)

#获取订单服务ip地址
def get_order_service_host():
    return get_request_host_url(REAG_DISCOVERY_CENTER_HOST,ORDER_SERVICE_HOST,REAG_DISCOVERY_CENTER_TOKEN)


#获取商品服务ip地址
def get_product_service_host():
    return get_request_host_url(REAG_DISCOVERY_CENTER_HOST,PRODUCT_SERVICE_HOST,REAG_DISCOVERY_CENTER_TOKEN)

#获取发货服务ip地址
def get_shipping_service_host():
    return get_request_host_url(REAG_DISCOVERY_CENTER_HOST,SHIPPING_SERVICE_HOST,REAG_DISCOVERY_CENTER_TOKEN)

#获取支付服务ip地址
def get_payment_service_host():
    return get_request_host_url(REAG_DISCOVERY_CENTER_HOST,PAYMENT_SERVICE_HOST,REAG_DISCOVERY_CENTER_TOKEN)


#获取钉钉服务ip地址
def get_dingtalk_service_host():
    return get_request_host_url(REAG_DISCOVERY_CENTER_HOST,DINGTALK_SERVICE_HOST,REAG_DISCOVERY_CENTER_TOKEN)


print(get_internal_account_service_host())
print(get_order_service_host())
print(get_shipping_service_host())


# 获取config配置文件：源用户信息
source_user = read_config.source_user(TEST_ENV)
target_user = read_config.target_user(TEST_ENV)

def source_user_id():
    return source_user.get('id')

def source_user_username():
    return source_user.get('username')

def source_user_email():
    return source_user.get('email')

def source_user_password():
    return source_user.get('password')

def test_phone_number():
    return os.environ['test_phone_number']

# 获取原用户登录token，避免测试用例中多次调用登录态都初始化函数，这里先定义变量
source_user_login_token_account_v2 = login_token_account_v2(TIGER_API_HOST, source_user_username(), source_user_password())
def source_user_login_token():
    return source_user_login_token_account_v2

# 目标用户信息
def target_user_id():
    return target_user.get('id')

def target_user_username():
    return target_user.get('username')

def target_user_password():
    return target_user.get('password')

# 获取内部账号配置数据
internal_source_user = read_config.internal_source_user(TEST_ENV)

def internal_source_user_email():
    return internal_source_user.get('email')

def internal_source_user_password():
    return internal_source_user.get('password')

def internal_source_user_id():
    return internal_source_user.get('id')

def internal_source_user_phone_number():
    return internal_source_user.get('phone_number')

def internal_source_user_department_id():
    return internal_source_user.get('department_id')

def internal_source_user_fish_id():
    return internal_source_user.get('relation_fish_id')

# 获取内部账号系统token
def internal_source_user_login_token():
    #login_token= login_token_internal_account(${INTERNAL_ACCOUNT_SERVICE_HOST()}, internal_source_user_email(), internal_source_user_password())
    login_token = generate_internal_account_token(get_internal_account_service_host(), internal_source_user_id())
    return login_token

# 读取内部账号 mysql 配置
def get_mysql_config_internal_account():
    mysql_config_internal_account = read_config.read_config_mysql(TEST_ENV, 'internal_account')
    global opmysql_internal_account
    opmysql_internal_account = OpMysql(host=mysql_config_internal_account['host'], user=mysql_config_internal_account['user'], password=mysql_config_internal_account['password'], database=mysql_config_internal_account['database'])

def internal_account_delete_two_step_verification(user_id):
    opmysql_internal_account.internal_account_delete_two_step_verification(user_id)

# 读取内部账号 redis 配置
def get_redis_config():
    redis_config = read_config.read_config_redis(TEST_ENV)
    global op_redis_internal_account
    op_redis_internal_account = OpRedis(host=redis_config['host'], port=redis_config['port'], password=redis_config['password'], db=2)

# 获取内部账号手机号验证码
def get_phone_number_captcha_internal_account(phone_number):
    return op_redis_internal_account.get_phone_number_captcha_internal_account(phone_number)

# 设置内部账号邮件发送验证码的总次数
def set_send_email_captcha_limit(email, value):
    return op_redis_internal_account.set_send_email_captcha_limit(email, value)

# 判断是否是dev或者test环境
def is_dev_or_test():
    return True if TEST_ENV not in ('staging', 'production') else False

# 判断是否是正式环境
def is_production():
    return True if TEST_ENV == 'production' else False

# 因为test中None会被解析为字符串，所以这里增加此函数
def is_none(source):
    return True if source == None else False

# 读获取虚拟商品配置信息
sku_config = read_config.sku(TEST_ENV)

def sku_number_config():
    return sku_config.get('sku_number')

def spu_number_config():
    return sku_config.get('spu_number')

def sku_price_config():
    return sku_config.get('price')

def spu_term_config():
    return sku_config.get('term_id')

def material_count_1_config():
    return sku_config.get('material_count_1')

def material_count_2_config():
    return sku_config.get('material_count_2')

def material_number_1_config():
    return sku_config.get('material_number_1')

def material_number_2_config():
    return sku_config.get('material_number_2')



# 读获取虚拟&实物商品配置信息
sku_physical_config = read_config.sku_physical(TEST_ENV)

def sku_physical_number_config():
    return sku_physical_config.get('sku_number')

def sku2_physical_number_config():
    return sku_physical_config.get('sku_number2')

def spu_physical_number_config():
    return sku_physical_config.get('spu_number')

def sku_physical_price_config():
    return sku_physical_config.get('price')


# 获取订金商品配置信息
sku_deposit_config = read_config.sku_deposit(TEST_ENV)

def sku_number_deposit():
    return sku_deposit_config.get('sku_number')

# 获取商品属性配置信息
attribute_config = read_config.attribute(TEST_ENV)

def attribute_id():
    return attribute_config.get('id')

def attribute_value_id():
    return attribute_config.get('value_id')
    

# 读取order配置信息
order_config = read_config.order(TEST_ENV)

def order_customerId_config():
    return order_config.get('customerId')

def order_placedBy_config():
    return order_config.get('placedBy')

def order_customerPhoneNumber_config():
    return order_config.get('customerPhoneNumber')

def order_handledById_config():
    return order_config.get('handledById')

def order_handledByName_config():
    return order_config.get('handledByName')

def has_track_shippingId_config():
    return order_config.get('shippingId')

def firstdepartmentId():
    return order_config.get('firstDepartmentId')


# 读取shippingInfo配置信息
shipping_config = read_config.shipping(TEST_ENV)

def shipping_departmentNumber_config():
    return shipping_config.get('departmentNumber')

def shipping_internal_userId_config():
    return shipping_config.get('internal_userId')

def order_warehouseCode_config():
    return shipping_config.get('warehouseCode')


# 随机生成交易流水号
def random_transaction_number():
    return "AutoTestTransaction"+str(int(time.time()))

#获取开始时间戳
def get_start_timestamp():
    return str(int(time.time())-5000)

#获取结束时间戳
def get_end_timestamp():
    return str(int(time.time())+5000)