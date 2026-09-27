#!/usr/bin/env python3
"""在宿主机运行：python3 smoke-test.py；独立浏览器上下文，不影响用户数据。"""
import json, threading, functools, http.server, pathlib, traceback
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent
checks=[]
def check(name, condition=True):
    if not condition: raise AssertionError(name)
    checks.append({'name':name,'status':'passed'})
class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Quiet,directory=str(ROOT)))
threading.Thread(target=server.serve_forever,daemon=True).start()
url=f'http://127.0.0.1:{server.server_port}/index.html'
result={'title':'某企业固定资产盘点演示系统','entry':'index.html','identity':'douyin','features':['资产登记与修改','虚构编号输入模拟扫码盘点','账实差异自动比对','一二三楼台账与实盘统计','搜索、楼层及状态筛选','分页列表','localStorage 持久化','筛选结果 CSV 导出','确认后重置演示数据','桌面与手机适配'],'tests':checks,'limitations':['演示数据仅当前浏览器保存，不支持多用户或跨设备同步','扫码为编号输入模拟，未接入摄像头或硬件','楼层分布依据台账登记楼层，未单独采集实物所在楼层','不提供真实后台、权限认证或审计服务','未进行几万条资产的性能压测','代码上传待补：未指定仓库及上传授权','外部预览地址由主控接入，未对外发布']}
try:
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
        context=browser.new_context(viewport={'width':1440,'height':1100},accept_downloads=True)
        page=context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.goto(url);page.wait_for_selector('#rows tr')
        check('初始统计：台账 110、实盘 83、差异 2 条、待盘 2 条',page.locator('#total').inner_text()=='110' and page.locator('#actual').inner_text()=='83' and page.locator('#diff').inner_text()=='2 条' and page.locator('#pending').inner_text()=='2 条')
        page.click('#add');page.fill('#code','XN-9001');page.fill('#assetName','演示测试设备');page.select_option('#floor','三楼');page.fill('#book','10');page.click('#assetForm button.primary')
        check('新增资产联动总数与三楼台账',page.locator('#total').inner_text()=='120' and '台账 32 / 实盘 10' in page.locator('[data-floor="三楼"]').inner_text())
        page.fill('#scanCode','XN-9001');page.click('#scanForm button');page.fill('#quantity','7');page.click('#countForm button.primary')
        check('模拟扫码实盘 7，盘亏 3，三楼实盘 17',page.locator('#actual').inner_text()=='90' and page.locator('#diff').inner_text()=='3 条' and '盘亏 4' in page.locator('#diffDetail').inner_text() and '实盘 17' in page.locator('[data-floor="三楼"]').inner_text())
        page.reload();check('刷新保存新增资产和实盘',page.locator('#total').inner_text()=='120' and page.locator('#actual').inner_text()=='90')
        page.click('[data-edit="XN-9001"]');page.select_option('#floor','二楼');page.fill('#book','7');page.click('#assetForm button.primary')
        check('修改台账及楼层即时消除差异并迁移统计',page.locator('#total').inner_text()=='117' and page.locator('#diff').inner_text()=='2 条' and '台账 63 / 实盘 49' in page.locator('[data-floor="二楼"]').inner_text())
        page.fill('#search','XN-9001');page.select_option('#floorFilter','二楼');page.select_option('#statusFilter','账实一致');check('组合筛选',page.locator('#rows tr').count()==1 and 'XN-9001' in page.locator('#rows').inner_text())
        with page.expect_download() as d: page.click('#export')
        data=pathlib.Path(d.value.path()).read_text(encoding='utf-8-sig');check('CSV 导出筛选后的真实数据', 'XN-9001' in data and 'XN-1001' not in data and '账实一致' in data)
        page.fill('#search','不存在');check('空结果提示','没有匹配资产' in page.locator('#rows').inner_text())
        page.fill('#scanCode','XN-0000');page.click('#scanForm button');check('未知编号提示','未找到' in page.locator('#scanError').inner_text())
        page.click('#add');page.fill('#code','XN-9001');page.fill('#assetName','演示重复设备');page.click('#assetForm button.primary');check('重复编号阻止保存','已存在' in page.locator('#assetError').inner_text());page.click('[data-close="assetDialog"]')
        page.fill('#scanCode','XN-9001');page.click('#scanForm button');page.fill('#quantity','-1');page.click('#countForm button.primary');check('负数实盘被阻止',page.locator('#countDialog').is_visible() and page.locator('#actual').inner_text()=='90');page.fill('#quantity','0');page.click('#countForm button.primary');check('零实盘有效',page.locator('#actual').inner_text()=='83')
        page.click('#reset');page.click('[data-close="resetDialog"]');check('取消重置保留数据',page.locator('#total').inner_text()=='117')
        page.click('#reset');page.click('#confirmReset');check('确认重置恢复初始数据',page.locator('#total').inner_text()=='110');page.reload();check('重置结果刷新后保存',page.locator('#total').inner_text()=='110')
        check('localStorage 键均使用项目专属前缀',page.evaluate('Object.keys(localStorage).every(k=>k.startsWith("development-11-"))'))
        for n in range(3):
            page.click('#add');page.fill('#code',f'XN-800{n}');page.fill('#assetName','演示分页设备');page.click('#assetForm button.primary')
        check('多于八条资产分页',page.locator('#rows tr').count()==8);page.click('#next');check('翻页有效',page.locator('#rows tr').count()==1)
        page.click('#reset');page.click('#confirmReset')
        page.locator('#toast').wait_for(state='hidden')
        page.screenshot(path=str(ROOT/'evidence-desktop.png'),full_page=True)
        page.set_viewport_size({'width':390,'height':844});check('手机页面无整体水平溢出',page.evaluate('document.documentElement.scrollWidth<=innerWidth'))
        page.click('#add');check('手机新增弹窗可操作',page.locator('#assetDialog').is_visible());page.click('[data-close="assetDialog"]');page.screenshot(path=str(ROOT/'evidence-mobile.png'),full_page=True)
        page.evaluate('localStorage.setItem("development-11-assets-v1","broken")');page.reload();check('损坏存储明确提示并防止静默覆盖',page.locator('#storageError').is_visible() and page.evaluate('localStorage.getItem("development-11-assets-v1")')=='broken')
        page.click('#reset');page.click('#confirmReset');check('确认重置可恢复损坏存储',not page.locator('#storageError').is_visible())
        check('无浏览器脚本异常',not errors)
        browser.close()
    result['test_status']='passed';result['test_environment']='宿主机 Chromium / Python Playwright，127.0.0.1 临时 HTTP 服务，独立浏览器上下文';result['evidence']=['evidence-desktop.png','evidence-mobile.png']
except Exception as e:
    result['test_status']='failed';result['test_error']=str(e);traceback.print_exc()
finally:
    server.shutdown();(ROOT/'development-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
if result['test_status']!='passed': raise SystemExit(1)
