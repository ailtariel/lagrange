<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
      clipped-left
    >
      <v-app-bar-nav-icon
        @click.stop="menu = !menu"
      ></v-app-bar-nav-icon>
      <v-app-bar-title>
        保底研发
      </v-app-bar-title>

      <v-spacer></v-spacer>

      <v-btn text>
        ver 1.0
      </v-btn>
    </v-app-bar>

    <v-main>
      <Research />
    </v-main>
  </v-app>
</template>

<script>
import Research from './components/research.vue';
import {
  defineComponent,
  ref,
  provide
} from '@vue/composition-api';

export default defineComponent({
  components:{
    Research
  },
  setup() {
    const menu = ref(true);
    provide('menu', menu);
    return {
      menu
    }
  },
  data(){
    return {

    }
  }
})
</script>
