<template>
  <v-app>
    <v-main>
      <Graph/>
    </v-main>
  </v-app>
</template>

<script>
import Graph from './components/Graph';

export default {
  name: 'App',
  components: {
    Graph,
  },
};
</script>
