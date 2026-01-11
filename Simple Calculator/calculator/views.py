from django.shortcuts import render

def index(request):
    result = ""
    expression = ""

    if request.method == "POST":
        expression = request.POST.get("expression", "")
        
        # Handle different buttons
        if "calculate" in request.POST:
            try:
                # Basic validation to prevent arbitrary code execution
                allowed_chars = set("0123456789+-*/. ")
                if not all(c in allowed_chars for c in expression):
                    result = "Error"
                else:
                    # Evaluate the expression
                    # eval() is used here for simplicity as requested for a basic calculator.
                    # In a production app, a proper parser should be used.
                    result = eval(expression)
            except Exception:
                result = "Error"
        elif "clear" in request.POST:
            expression = ""
            result = ""
        else:
            # For number/operator buttons if handled via submit (though usually JS handles appending)
            # We will assume JS handles appending to the input, and "calculate" submits the full string.
            pass

    return render(request, "calculator/index.html", {"result": result, "expression": expression})
