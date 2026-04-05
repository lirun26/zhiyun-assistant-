#!/usr/bin/env python3
"""
药师帮爬虫 - 基础版
功能：商品信息、供应商信息、订单数据
"""

import requests
import json
import time
import re
from typing import List, Dict, Optional
from urllib.parse import urlencode

class YaobangbangCrawler:
    """药师帮爬虫类"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://www.yaobang.com/'
        })
        self.base_url = 'https://www.yaobang.com'
        self.is_logged_in = False
        
    def login(self, phone: str, password: str) -> bool:
        """
        登录药师帮
        注意：验证码需要手动处理
        """
        print(f"📱 正在登录药师帮...")
        
        # TODO: 根据实际登录接口调整
        login_url = f"{self.base_url}/api/user/login"
        
        data = {
            'phone': phone,
            'password': password,
            'loginType': 'password'
        }
        
        try:
            response = self.session.post(login_url, data=data, timeout=30)
            result = response.json()
            
            if result.get('code') == 0 or result.get('success'):
                self.is_logged_in = True
                print("✅ 登录成功！")
                return True
            else:
                print(f"❌ 登录失败: {result.get('message', '未知错误')}")
                return False
                
        except Exception as e:
            print(f"❌ 登录异常: {e}")
            return False
    
    def get_product_list(self, keyword: str, page: int = 1, page_size: int = 20) -> List[Dict]:
        """
        获取商品列表
        """
        if not self.is_logged_in:
            print("⚠️ 请先登录")
            return []
        
        # TODO: 根据实际API调整
        url = f"{self.base_url}/api/product/search"
        params = {
            'keyword': keyword,
            'page': page,
            'pageSize': page_size
        }
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            data = response.json()
            
            if data.get('code') == 0:
                return data.get('data', {}).get('list', [])
            else:
                print(f"❌ 获取商品列表失败: {data.get('message')}")
                return []
                
        except Exception as e:
            print(f"❌ 请求异常: {e}")
            return []
    
    def get_product_detail(self, product_id: str) -> Optional[Dict]:
        """
        获取商品详情
        """
        if not self.is_logged_in:
            print("⚠️ 请先登录")
            return None
        
        # TODO: 根据实际API调整
        url = f"{self.base_url}/api/product/detail/{product_id}"
        
        try:
            response = self.session.get(url, timeout=30)
            data = response.json()
            
            if data.get('code') == 0:
                return data.get('data', {})
            else:
                print(f"❌ 获取商品详情失败: {data.get('message')}")
                return None
                
        except Exception as e:
            print(f"❌ 请求异常: {e}")
            return None
    
    def get_supplier_list(self, page: int = 1, page_size: int = 20) -> List[Dict]:
        """
        获取供应商列表
        """
        if not self.is_logged_in:
            print("⚠️ 请先登录")
            return []
        
        # TODO: 根据实际API调整
        url = f"{self.base_url}/api/supplier/list"
        params = {
            'page': page,
            'pageSize': page_size
        }
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            data = response.json()
            
            if data.get('code') == 0:
                return data.get('data', {}).get('list', [])
            else:
                print(f"❌ 获取供应商列表失败: {data.get('message')}")
                return []
                
        except Exception as e:
            print(f"❌ 请求异常: {e}")
            return []
    
    def get_order_list(self, status: str = 'all', page: int = 1, page_size: int = 20) -> List[Dict]:
        """
        获取订单列表
        status: all-全部, pending-待付款, paid-已付款, shipped-已发货, completed-已完成
        """
        if not self.is_logged_in:
            print("⚠️ 请先登录")
            return []
        
        # TODO: 根据实际API调整
        url = f"{self.base_url}/api/order/list"
        params = {
            'status': status,
            'page': page,
            'pageSize': page_size
        }
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            data = response.json()
            
            if data.get('code') == 0:
                return data.get('data', {}).get('list', [])
            else:
                print(f"❌ 获取订单列表失败: {data.get('message')}")
                return []
                
        except Exception as e:
            print(f"❌ 请求异常: {e}")
            return []
    
    def export_to_json(self, data: List[Dict], filename: str):
        """导出数据到JSON文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ 数据已导出到 {filename}")


def main():
    """使用示例"""
    crawler = YaobangbangCrawler()
    
    # 登录（请替换为你的账号密码）
    # 建议：从环境变量读取，不要硬编码
    phone = input("请输入手机号: ").strip()
    password = input("请输入密码: ").strip()
    
    if not crawler.login(phone, password):
        print("❌ 登录失败，程序退出")
        return
    
    while True:
        print("\n" + "="*50)
        print("📋 药师帮数据爬虫")
        print("="*50)
        print("1. 搜索商品")
        print("2. 获取供应商列表")
        print("3. 获取订单列表")
        print("0. 退出")
        print("="*50)
        
        choice = input("请选择功能 (0-3): ").strip()
        
        if choice == '1':
            keyword = input("请输入搜索关键词: ").strip()
            products = crawler.get_product_list(keyword)
            print(f"\n获取到 {len(products)} 条商品数据")
            if products:
                crawler.export_to_json(products, 'products.json')
                
        elif choice == '2':
            suppliers = crawler.get_supplier_list()
            print(f"\n获取到 {len(suppliers)} 条供应商数据")
            if suppliers:
                crawler.export_to_json(suppliers, 'suppliers.json')
                
        elif choice == '3':
            orders = crawler.get_order_list()
            print(f"\n获取到 {len(orders)} 条订单数据")
            if orders:
                crawler.export_to_json(orders, 'orders.json')
                
        elif choice == '0':
            print("👋 再见！")
            break
            
        else:
            print("⚠️ 无效选择")


if __name__ == '__main__':
    main()
