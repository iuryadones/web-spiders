d = db.getCollection('dados_abertos').find({}).toArray();
d.forEach(function(f){
    if (f['acoes'].length > 15) {
        print(f['acoes'].length)
    } 
    else if (f['acoes'].lenght < 15){
        print(f['acoes'].length)
    }
})