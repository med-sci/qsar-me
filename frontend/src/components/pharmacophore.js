// ADD ERROR HANDLER deal with script loading

function create3Dmodel(id, pharmacophore){
    const url = `https://mapex-test.s3.amazonaws.com/molecules_${id}.sdf`
    import('jquery').then(($)=>{
        import('3dmol/build/3Dmol-nojquery').then(($3Dmol)=>{
            let viewer = $3Dmol.createViewer('mol-col')
            $.get(url, function(data){
                let v = viewer 
                v.addModels(data, 'sdf')
                v.setStyle({}, {stick:{}})
                for (let p of pharmacophore){
                    let radius = 1.25
                    let wireframe = true
                    let color = "purple"
                    if (p.label === 'Donors'){
                        radius = 1
                        color = 'blue'
                    }
                    let s = v.addSphere({'radius':radius, 'color':color, 'center':{
                        x:p.x,
                        y:p.y,
                        z:p.z
                    }})
                    s.wireframe = wireframe
                }
                v.zoom(3,1000)
                v.render()
            })
        })
    })
}

export default async function getPharmacophore(id){
    const url = `http://127.0.0.1:8000/api/pharmacophores/?model=${id}`
    const response = await fetch(url, {
        method:'get',
        'Contetent-Type':'application/json'
    });
    const pharmacophore = await response.json();
    console.log(pharmacophore)
    create3Dmodel(id, pharmacophore)
}