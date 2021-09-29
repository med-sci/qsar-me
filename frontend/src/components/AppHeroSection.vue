<template>
    <section class="hero bg-light">
        <div class="container-fluid h-100 align-items-center"  >
            <div class="row h-100">
                <div class="col-12 align-self-center text-center">
                    <h3 class="display-3"> Welcome to </h3>
                    <h1 class="display-1 fw-bold">QSAR.ME</h1>
                    <hr class="w-100">
                    <p class="fs-5 display-1">A free pharmacophore building tool. 
                        <br> Build your pharmacophore easy, only SMILES information required</p>
                </div>
                <div class="col-12 text-center">
                    <button class="btn btn-primary mx-2"
                    @click="$emit('start')">GET STARTED</button>
                    <button class="btn btn btn-outline-secondary mx-2">LEARN MORE</button>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
    export default {
        emits:['start']
    }
</script>

<style scoped>
.hero{
    height: 500px;
}

</style>