<template>
  <v-app>
      <v-main class="mb-5">
      <v-slide-x-transition mode="out-in">  
        <router-view></router-view>
      </v-slide-x-transition>
    </v-main>
  </v-app>
</template>

<script>

export default {
  name: 'App',

  data: () => ({
    drawer: false,
    pages:[

    ]
  }),
};
</script>
