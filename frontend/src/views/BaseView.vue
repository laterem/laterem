<template>
  <body>
    <div>
      <!-- Here must go Menu component -->
      <!-- <aside id="menu">
                {% block menu %}
                {% endblock %}
            </aside> -->
      <!-- Here must go Main Page Content component -->
      <!-- {% if task_list %}
                <aside id="content" style="bottom: 30px;">
            {% else %}
                <aside id="content">
            {% endif %}
                {% block content %}
                {% endblock %}
            </aside> -->
      <!-- It modifies content view if task list needed -->
      <!-- {% if task_list %}
                <aside id="foot">
                    <div>
                        {% block foot %}
                        {% endblock %}
                    </div>
                </aside>
            {% endif %} -->
    </div>
    <!-- <script src="{% static 'js/caret-manager.js' %}?{% cache_bust %}"></script> -->
    <!-- {% render_bundle 'app' 'js' %} -->
  </body>
  <!-- Header component -->
  <!-- <header role="banner" class="header">
    
        <div class="header">
            <a id="main-icon" class="header button" href="/">
                {% include "icons/main-icon.html" %}
            </a>
            <a href="/" class="header">
                <h1 class="header">Laterem</h1>
            </a>
        </div>

        <div style="justify-self: end;" class="header">
            <a href="/report_a_bug/" class="button wrong">Сообщить об ошибке</a>
        </div>

        <form method="post" class="dropdown-toggle-form">
            {% csrf_token %}
            <div style="justify-self: end; padding-right: 5px;" class="header dropdown-toggle-keeper">
                <p id="main-icon" class="header button dropdown-toggle" style="margin-right:5px; width: 5mm; height: 5mm; grid-column: 1; justify-self: end;">
                    {% include "icons/user-icon.html" %}
                </p>
                <p class="dropdown-toggle" style="grid-column: 2;">{{user.username}}</p>
                <ul class="dropdown-content" id="header-dropdown-item" style="grid-row: 2; grid-column-start: 1; grid-column-end: 3;">
                    <li><a href="/profile">Профиль</a></li>
                    <li style="display: block;"><hr/></li>
                    <li><p>
                        Тема
                        <select name="color-theme">
                            {% for theme_option in all_themes %}
                                {% if theme_option == theme %}
                                    <option selected>{{ theme_option }}</option>
                                {% else %}
                                    <option>{{ theme_option }}</option>
                                {% endif %}
                            {% endfor %}
                        </select><button type="submit" class="button" name="change-color-theme">Изменить</button>
                    </p></li>
                    <li style="display: block;"><hr/></li>
                    <li><a class="button" href="/logout">Выйти</a></li>
                </ul>
            </div>
        </form>

        <script src="{% static 'js/dropdown-manage.js' %}?{% cache_bust %}"></script>

        <div width="100vh" style="background-color: var(--header-gradient-bottom); height: 1px; position: fixxed; bottom: 0px;"></div>
    
    </header> -->
</template>
