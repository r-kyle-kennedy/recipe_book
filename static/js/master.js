let ingredientCounter = 1;
function addIngredient() {
    const container = document.getElementById('ingredientContainer');
    const newRow = document.createElement('div');
    newRow.className = 'ingredient-row';
    newRow.innerHTML = `
        <input type="text" name="ingredient${ingredientCounter}" placeholder="Enter ingredient" required>
        <input type="text" name="amount${ingredientCounter}" placeholder="Enter amount: ie 1 cup" required>
        <input type="text" name="url${ingredientCounter}" placeholder="URL" required>
        <input type="number" name="calories${ingredientCounter}" placeholder="Calories" required>
        <input type="number" name="protein${ingredientCounter}" placeholder="Grams of Protein" required>
        <input type="number" name="fat${ingredientCounter}" placeholder="Grams of Fat" required>
        <input type="number" name="carbs${ingredientCounter}" placeholder="Grams of Carbohydrates" required>
        <button type="button" class="remove-btn" onclick="removeIngredient(this)">Remove</button>
    `;
    container.appendChild(newRow);
    ingredientCounter++;
}

function removeIngredient(button) {
    const container = document.getElementById('ingredientContainer');
    // Don't allow removing if it's the last ingredient
    if (container.children.length > 1) {
        button.parentElement.remove();
    }
}

function buildForm(recipe) {
  console.log(recipe)
  ingredients=Object.keys(recipe['ingredients'])
  const container = document.getElementById('ingredientContainer');
  for (var i = 0; i < ingredients.length; i++) {
    const newRow = document.createElement('div');
    newRow.className = 'ingredient-row';
    newRow.innerHTML = `
    <input type="text" name="ingredient${i}" placeholder="Enter ingredient" value="${ingredients[i]}" required>
    <input type="text" name="amount${ingredientCounter}" placeholder="Enter amount: ie 1 cup" value="${recipe['ingredients'][ingredients[i]]['amount']}" required>
    <input type="text" name="url${ingredientCounter}" placeholder="URL" value="${recipe['ingredients'][ingredients[i]]['url']}" required>
    <input type="number" name="calories${ingredientCounter}" placeholder="Calories" value="${recipe['ingredients'][ingredients[i]]['calories']}" required>
    <input type="number" name="protein${ingredientCounter}" placeholder="Grams of Protein" value="${recipe['ingredients'][ingredients[i]]['macros']['protein']}" required>
    <input type="number" name="fat${ingredientCounter}" placeholder="Grams of Fat" value="${recipe['ingredients'][ingredients[i]]['macros']['fat']}" required>
    <input type="number" name="carbs${ingredientCounter}" placeholder="Grams of Carbohydrates" value="${recipe['ingredients'][ingredients[i]]['macros']['carbs']}" required>
    <button type="button" class="remove-btn" onclick="removeIngredient(this)">Remove</button>
    `;
    container.appendChild(newRow);
    ingredientCounter++;
  }
}
