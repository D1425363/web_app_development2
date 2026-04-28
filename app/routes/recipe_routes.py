from flask import Blueprint, render_template, request, redirect, url_for, abort, flash
from ..models.recipe import Recipe
from ..models.ingredient import Ingredient
from ..models.step import Step
from ..models.note import Note

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/')
@recipe_bp.route('/recipes')
def index():
    """
    顯示所有食譜列表。
    支援標籤過濾。
    """
    tag_filter = request.args.get('tag')
    all_recipes = Recipe.get_all()
    
    if tag_filter:
        # 簡單的標籤過濾邏輯（在 Python 端過濾）
        filtered_recipes = [r for r in all_recipes if tag_filter in (r.get('tags') or '')]
        return render_template('recipes/index.html', recipes=filtered_recipes, current_tag=tag_filter)
    
    return render_template('recipes/index.html', recipes=all_recipes)

@recipe_bp.route('/recipes/new', methods=['GET', 'POST'])
def new_recipe():
    """
    新增食譜。
    GET: 顯示表單。
    POST: 儲存資料。
    """
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        tags = request.form.get('tags')
        
        # 取得多個材料與步驟
        ingredient_names = request.form.getlist('ingredient_name[]')
        ingredient_amounts = request.form.getlist('ingredient_amount[]')
        step_instructions = request.form.getlist('step_instruction[]')

        if not title:
            flash('食譜標題為必填欄位！')
            return render_template('recipes/new.html')

        # 1. 建立食譜主體
        recipe_id = Recipe.create(title, description, tags)
        
        if recipe_id:
            # 2. 建立材料
            for name, amount in zip(ingredient_names, ingredient_amounts):
                if name.strip():
                    Ingredient.create(recipe_id, name, amount)
            
            # 3. 建立步驟
            for i, instr in enumerate(step_instructions):
                if instr.strip():
                    Step.create(recipe_id, i + 1, instr)
            
            flash('食譜建立成功！')
            return redirect(url_for('recipe.detail', recipe_id=recipe_id))
        else:
            flash('建立食譜時發生錯誤。')
            return render_template('recipes/new.html')

    return render_template('recipes/new.html')

@recipe_bp.route('/recipes/<int:recipe_id>')
def detail(recipe_id):
    """
    食譜詳情頁面。
    """
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe:
        abort(404)
    
    ingredients = Ingredient.get_by_recipe(recipe_id)
    steps = Step.get_by_recipe(recipe_id)
    notes = Note.get_by_recipe(recipe_id)
    
    return render_template('recipes/detail.html', 
                           recipe=recipe, 
                           ingredients=ingredients, 
                           steps=steps, 
                           notes=notes)

@recipe_bp.route('/recipes/<int:recipe_id>/edit', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    """
    編輯食譜。
    """
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe:
        abort(404)

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        tags = request.form.get('tags')
        
        ingredient_names = request.form.getlist('ingredient_name[]')
        ingredient_amounts = request.form.getlist('ingredient_amount[]')
        step_instructions = request.form.getlist('step_instruction[]')

        if not title:
            flash('食譜標題不能為空！')
            return render_template('recipes/edit.html', recipe=recipe)

        # 更新食譜主體
        if Recipe.update(recipe_id, title, description, tags):
            # 更新材料與步驟（採先刪後增策略）
            Ingredient.delete_by_recipe(recipe_id)
            for name, amount in zip(ingredient_names, ingredient_amounts):
                if name.strip():
                    Ingredient.create(recipe_id, name, amount)
            
            Step.delete_by_recipe(recipe_id)
            for i, instr in enumerate(step_instructions):
                if instr.strip():
                    Step.create(recipe_id, i + 1, instr)
            
            flash('食譜更新成功！')
            return redirect(url_for('recipe.detail', recipe_id=recipe_id))
        else:
            flash('更新食譜時發生錯誤。')

    # GET 請求時需抓取現有材料與步驟
    ingredients = Ingredient.get_by_recipe(recipe_id)
    steps = Step.get_by_recipe(recipe_id)
    
    return render_template('recipes/edit.html', 
                           recipe=recipe, 
                           ingredients=ingredients, 
                           steps=steps)

@recipe_bp.route('/recipes/<int:recipe_id>/delete', methods=['POST'])
def delete_recipe(recipe_id):
    """
    刪除食譜。
    """
    if Recipe.delete(recipe_id):
        flash('食譜已刪除。')
    else:
        flash('刪除食譜時發生錯誤。')
    return redirect(url_for('recipe.index'))

@recipe_bp.route('/recipes/<int:recipe_id>/notes', methods=['POST'])
def add_note(recipe_id):
    """
    新增筆記。
    """
    content = request.form.get('content')
    rating = request.form.get('rating')
    
    if content:
        Note.create(recipe_id, content, rating)
        flash('筆記已儲存。')
    else:
        flash('筆記內容不能為空。')
        
    return redirect(url_for('recipe.detail', recipe_id=recipe_id))

@recipe_bp.route('/recipes/<int:recipe_id>/shopping-list')
def shopping_list(recipe_id):
    """
    產生購物清單。
    """
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe:
        abort(404)
        
    ingredients = Ingredient.get_by_recipe(recipe_id)
    return render_template('recipes/shopping_list.html', recipe=recipe, ingredients=ingredients)
