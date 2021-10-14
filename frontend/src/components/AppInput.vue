<template>
    <section class="bg-light text-light">
        <div class="container-md py-3 bg-light text-dark">
            <div class="row justify-content-center align-items-top">
                <div class="col-12 col-md-7">
                    <h3 class="display-6 ">{{titles[idx]}}</h3>
                </div>
            </div>
            <div class="row justify-content-center align-items-top">
                <div class="col-12 col-md-7">
                    <form @submit.prevent=""
                    @keypress.enter.prevent="next(idx)">
                        <smiles-input v-if="idx==0" :type="type" v-model="smiles"></smiles-input>
                        <div class="mb-3" v-else-if="idx==1">
                            <config-input 
                            v-model="nConfs"
                            text="Number of conformations for each molecule"
                            label="confs"
                            :isValid="nConfs >=10 & nConfs <=100 ? '':'is-invalid'"
                            min="10"
                            max="100"></config-input>
                            <config-input 
                            v-model="nInds"
                            :isValid="nInds >=5 & nInds <=50 ? '':'is-invalid'"
                            text="Number of individuals in generation"
                            label="inds"
                            min="5"
                            max="50"></config-input>
                            <config-input 
                            :isValid="mChance >=0 & mChance <=1 ? '':'is-invalid'"
                            v-model="mChance"
                            text="Mutation rate"
                            label="mut"
                            min="0"
                            max="1"
                            step="0.01"></config-input>
                            <config-input 
                            v-model="nGens"
                            :isValid="nGens >=10 & nGens <=500 ? '':'is-invalid'"
                            text="Number of generations"
                            label="gens"
                            min="10"
                            max="500"></config-input>
                        </div>
                        <email-input v-else-if="idx==2"
                        v-model="email"
                        :type="isMailValid ? '':'is-invalid' "></email-input>
                    <button type="submit" 
                    class="btn btn-primary mx-2" 
                    :disabled="idx == 0"
                    @click="back(idx)">Back</button>
                    <button type="submit" 
                    class="btn btn-primary"
                    v-if="idx !=2"
                    @click="next(idx)">Next</button>
                    <button v-else class="btn btn-success"
                    @click="submit">submit</button>
                    </form>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
//add pharmacophore distance info
import SmilesInput from './parts/SmilesInput.vue'
import ConfigInput from './parts/ConfigInput.vue'
import EmailInput from './parts/EmailInput.vue'
    export default {
        data(){
            return{
                idx: 0,
                titles:['Input smiles here',
                'Configue model properties',
                'Enter email adress'],
                smiles:'',
                nConfs: 50,
                nInds:10,
                mChance:0.3,
                nGens: 100,
                smilesCorrect:null,
                type:'',
                configCheck:[],
                email:'',
                isMailValid:true
            }
        },
        methods:{
            back(idx){
                this.idx = idx-1
            },
           async next(idx){
                if (idx==0){
                    await this.validateSmiles()
                    if (this.smilesCorrect){
                        this.idx = idx+1
                        this.type = 'is-valid'
                    }else{
                        this.type = 'is-invalid'
                    }
                }else if (idx===1){
                    this.configCheck=[]
                    this.confCheker()
                    if (this.configCheck.includes(false)){
                        this.idx = idx
                    }else{
                        this.idx = idx+1
                    }
                    
                }

            },
            showSmiles(){
                console.log(this.smiles)
            },
            async validateSmiles(){
                const res = await fetch('http://127.0.0.1:8000/api/validation/',{
                    method:'POST',
                    headers:{
                        'Content-Type':'application/json'
                    },
                    body: JSON.stringify({'smiles': this.smiles})
                }) 
                const status = await res.json()
                if (status.status === 'OK'){
                    this.smilesCorrect = true
                } else if (status.status === 'ERROR') {
                    this.smilesCorrect = false
                }else{
                    console.log(status)
                }
            },
            confCheker(){
                if (this.nConfs>=10 & this.nConfs<=100){
                    this.configCheck.push(true)
                }else{
                    this.configCheck.push(false)
                }
                if (this.nInds>=5 & this.nInds<=50){
                    this.configCheck.push(true)
                }else{
                    this.configCheck.push(false)
                }
                if (this.mChance>=0 & this.mChance<=1){
                    this.configCheck.push(true)
                }else{
                    this.configCheck.push(false)
                }
                if (this.nGens>=5 & this.nGens<=500){
                    this.configCheck.push(true)
                }else{
                    this.configCheck.push(false)
                }
            },
            submit(){
                if (this.email.includes('@')){
                    this.isMailValid = true
                    this.sendData()
                }else{
                    this.isMailValid = false
                }
            },
            async sendData(){
                const res = await fetch('http://localhost:8000/api/properties/',{
                    method:'POST',
                    headers:{
                        'Content-Type':'application/json'
                    },
                    body: JSON.stringify(
                        {
                            "smiles": this.smiles,
                            "num_inds": this.nInds,
                            "num_confs": this.nConfs,
                            "mutation_chance": this.mChance,
                            "generations": this.nGens,
                            "use_crippen": false,
                            "email": this.email
                        }
                    )
                })
                console.log(res.json())
            }
        },
        components:{
            SmilesInput,
            ConfigInput,
            EmailInput
        }
    }
</script>

<style lang="scss" scoped>

</style>