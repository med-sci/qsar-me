<template>
  <div>
      <app-hero-section></app-hero-section>
      <app-info-section></app-info-section>
      <app-input></app-input>
  </div>
</template>

<script>
import AppHeroSection from './AppHeroSection.vue'
import AppInfoSection from './AppInfoSection.vue'
import AppInput from './AppInput.vue'

export default {
  name: 'App',
  components: {
    AppHeroSection,
    AppInfoSection,
    AppInput,
  }
}
</script>

<style>

</style>
