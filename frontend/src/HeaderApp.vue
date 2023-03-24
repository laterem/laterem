<template>
  <header role="banner">
    <div>
      <router-link id="main-icon" class="button" to="/">
        <mainIcon style="width: 2rem" />
      </router-link>
      <router-link to="/">
        <h1>Laterem</h1>
      </router-link>
    </div>

    <div style="justify-self: end">
      <router-link to="/report_a_bug/" class="button wrong"
        >Сообщить об ошибке</router-link
      >
    </div>

    <form method="post" class="dropdown-toggle-form">
      <div
        style="
          justify-self: end;
          padding-right: 5px;
          display: grid;
          grid-template-rows: 60px auto;
          align-items: center;
          cursor: pointer;
        "
        class="dropdown-toggle-keeper"
        @click="dropdownIsActive = !dropdownIsActive"
      >
        <p
          id="main-icon"
          class="button dropdown-toggle"
          style="margin-right: 5px"
        >
          <userIcon style="width: 1.5rem" />
        </p>
        <p class="dropdown-toggle" style="grid-column: 2">
          <!--{{user.username}}-->
        </p>
        <ul
          class="dropdown-content"
          id="header-dropdown-item"
          style="grid-row: 2; grid-column-start: 1; grid-column-end: 3"
          v-show="dropdownIsActive"
        >
          <li><router-link to="/profile">Профиль</router-link></li>
          <li style="display: block"><hr /></li>
          <li>
            <p>
              Тема
              <select name="color-theme">
                <!-- Here must go theme list -->
                <!-- {% for theme_option in all_themes %}
                        {% if theme_option == theme %}
                            <option selected>{{ theme_option }}</option>
                        {% else %}
                            <option>{{ theme_option }}</option>
                        {% endif %}
                    {% endfor %} --></select
              ><button type="submit" class="button" name="change-color-theme">
                Изменить
              </button>
            </p>
          </li>
          <li style="display: block"><hr /></li>
          <li><router-link class="button" to="/logout">Выйти</router-link></li>
        </ul>
      </div>
    </form>

    <!-- <script src="{% static 'js/dropdown-manage.js' %}?{% cache_bust %}"></script> -->

    <div
      width="100vh"
      style="
        background-color: var(--header-gradient-bottom);
        height: 1px;
        position: fixed;
        bottom: 0px;
      "
    ></div>
  </header>
</template>

<script>
import mainIcon from "@/assets/icons/main-icon.vue";
import userIcon from "@/assets/icons/user-icon.vue";

export default {
  data() {
    return {
      dropdownIsActive: false,
    };
  },
  components: {
    mainIcon: mainIcon,
    userIcon: userIcon,
  },
};
</script>

<style scoped>
* {
  display: flex;
  align-self: center;
  align-items: center;
}

p {
  margin: 0;
}

header {
  top: 0;
  width: 100%;
  height: 60px;
  padding: 0;
  white-space: nowrap;
  position: fixed;
  background: inherit;
  display: grid;
  grid-template-columns: auto repeat(2, min-content);
  grid-template-rows: 100% max-content;
  background-image: linear-gradient(
    var(--header-gradient-top),
    var(--header-gradient-bottom)
  );
}

button {
  border-radius: 20px;
  padding: 5px 10px;
  box-shadow: none;
}

h1 {
  font-family: "Agency FB";
  margin: 0px;
}

hr {
  background-color: var(--header-gradient-bottom);
  border-color: var(--header-gradient-bottom);
  width: 100%;
  display: block;
}

#header-dropdown-item * {
  display: flex;
  padding: 5px;
  background-color: transparent;
}

#header-dropdown-item a,
#header-dropdown-item button {
  color: var(--body-font-color);
  text-decoration: none;
  border-radius: 5px;
}

#header-dropdown-item *:hover {
  background-color: var(--content-hover-color);
}

#header-dropdown-item hr {
  display: block;
  padding: 0;
}

#main-icon {
  margin: 10px;
  width: auto;
  padding: 5px;
  padding-bottom: 2px;
  border-radius: 30%;
  background: transparent;
  position: relative;
  box-shadow: none;
}
</style>
