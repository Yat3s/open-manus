#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import logging
import sys
import os
from rich.console import Console
from datetime import datetime

# 添加src目录到Python路径，这是关键
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "src")
sys.path.insert(0, src_path)

# 设置日志级别
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("test_plan_searches")

# 导入DeepResearchManager
try:
    from core.deep_research.manager import DeepResearchManager
    print("成功导入DeepResearchManager")
except ImportError as e:
    logger.error(f"导入错误: {str(e)}")
    print(f"导入错误: {str(e)}")
    print(f"当前Python路径: {sys.path}")
    sys.exit(1)

async def test_plan_searches(query: str):
    """测试 _plan_searches 方法的异步函数"""
    # 创建控制台对象用于彩色输出
    console = Console()
    console.print("[bold green]开始测试 _plan_searches 方法[/bold green]")
    
    # 创建 DeepResearchManager 实例
    manager = DeepResearchManager()
    
    # 添加当前年份到查询中，确保获取最新信息
    console.print(f"[bold blue]原始查询:[/bold blue] {query}")
    
    try:
        # 调用 _plan_searches 方法
        console.print("[yellow]正在规划搜索...[/yellow]")
        search_plan = await manager._plan_searches(query)
        
        # 打印搜索计划结果
        console.print("[bold green]搜索计划生成成功！[/bold green]")
        console.print(f"[blue]计划了 {len(search_plan.searches)} 个搜索[/blue]")
        
        # 打印每个搜索项的详细信息
        for i, search_item in enumerate(search_plan.searches, 1):
            console.print(f"\n[bold]搜索 #{i}[/bold]")
            console.print(f"查询: {search_item.query}")
            console.print(f"原因: {search_item.reason}")
            
    except Exception as e:
        console.print(f"[bold red]测试失败: {str(e)}[/bold red]")
        logger.error(f"测试出错: {e}", exc_info=True)

if __name__ == "__main__":
    """主函数，运行测试"""
    console = Console()
    console.print("[bold purple]===== DeepResearchManager._plan_searches 测试 =====[/bold purple]")
    
    # 运行异步测试函数
    asyncio.run(test_plan_searches("Microsoft"))
    
    console.print("[bold purple]===== 测试完成 =====[/bold purple]") 