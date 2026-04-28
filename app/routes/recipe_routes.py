from flask import Blueprint, render_template, request, redirect, url_for, abort

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/')
@recipe_bp.route('/recipes')
def index():
    """
    顯示所有食譜列表。
    輸入: 可選 URL 參數 ?tag=xxx 用於標籤過濾。
    邏輯: 呼叫 Recipe.get_all()。
    輸出: 渲染 recipes/index.html。
    """
    pass

@recipe_bp.route('/recipes/new', methods=['GET', 'POST'])
def new_recipe():
    """
    GET: 顯示新增食譜表單。
    POST: 接收表單資料，呼叫 Model 建立食譜、材料與步驟，成功後重導向至詳情頁。
    """
    pass

@recipe_bp.route('/recipes/<int:recipe_id>')
def detail(recipe_id):
    """
    顯示單筆食譜詳細內容。
    邏輯: 呼叫 Recipe.get_by_id(), Ingredient.get_by_recipe(), Step.get_by_recipe(), Note.get_by_recipe()
    輸出: 渲染 recipes/detail.html。如果找不到回傳 404。
    """
    pass

@recipe_bp.route('/recipes/<int:recipe_id>/edit', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    """
    GET: 取得現有食譜資料並顯示編輯表單。
    POST: 接收表單修改後的資料，更新 DB，成功後重導向至詳情頁。
    """
    pass

@recipe_bp.route('/recipes/<int:recipe_id>/delete', methods=['POST'])
def delete_recipe(recipe_id):
    """
    刪除食譜。
    邏輯: 呼叫 Recipe.delete(recipe_id) 刪除食譜及其關聯資料。
    輸出: 重導向至首頁。
    """
    pass

@recipe_bp.route('/recipes/<int:recipe_id>/notes', methods=['POST'])
def add_note(recipe_id):
    """
    新增食譜筆記與評價。
    邏輯: 接收 content 與 rating 表單，呼叫 Note.create()。
    輸出: 重導向回食譜詳情頁。
    """
    pass

@recipe_bp.route('/recipes/<int:recipe_id>/shopping-list')
def shopping_list(recipe_id):
    """
    顯示該食譜所需的材料購物清單。
    邏輯: 呼叫 Ingredient.get_by_recipe() 取得材料。
    輸出: 渲染 recipes/shopping_list.html。
    """
    pass
