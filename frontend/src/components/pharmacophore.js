// ADD ERROR HANDLER deal with script loading
const pharmacophore = [
    {
        'label': 'Aromatic',
        'center': {
            'x':-6.89,
            'y':0.75,
            'z':0.35
        }
    },
    {
        'label': 'Aromatic',
        'center': {
            'x':1.32,
            'y':2.91,
            'z':-1.49
        }
    },
    {
    'label': 'Hydrogen Donor',
        'center': {
            'x':-0.4217,
            'y':0.4795,
            'z':0.6395
        }
    }
]

const url = 'https://mapex-test.s3.amazonaws.com/molecules_12.sdf'

export default import('jquery').then(($)=>{
    import('3dmol/build/3Dmol-nojquery').then(($3Dmol)=>{
        let viewer = $3Dmol.createViewer('mol-col')
        $.get(url, function(data){
            let v = viewer 
            console.log(data)
            v.addModels(data, 'sdf')
            v.setStyle({}, {stick:{}})
            for (let p of pharmacophore){
                let radius = 1.25
                let wireframe = true
                let color = "purple"
                if (p.label === 'Hydrogen Donor'){
                    radius = 1
                    color = 'blue'
                }
                let s = v.addSphere({'radius':radius, 'color':color, 'center':{
                    x:p.center.x,
                    y:p.center.y,
                    z:p.center.z
                }})
                s.wireframe = wireframe
            }
            v.zoom(5,1000)
            v.render()
        })
    })
})