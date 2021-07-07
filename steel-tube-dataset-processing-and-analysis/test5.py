import json
if __name__=='__main__':
    label_names=['a','b','c']
    bndboxes3=[{'xmin':1,'xmax':2,'ymin':3,'ymax':4},{'xmin':5,'xmax':6,'ymin':7,'ymax':8},{'xmin':9,'xmax':10,'ymin':11,'ymax':12}]
    nw3=100
    nh3=50
    obj=[]
    for i in range(len(bndboxes3)):
        obj.append({"name":label_names[i],"bndbox":bndboxes3[i]})
    json_obj={
        "path": "",
        "outputs": {
            "object": obj
        },
        "time_labeled": 0,
        "labeled": True,
        "size": {
            "width": nw3,
            "height": nh3,
            "depth": 3
        }
    }
    rotate_json_path='test5.json'.replace('.json','(rotate).json')
    f=open(rotate_json_path,'w')
    json.dump(json_obj,f)
    f.close()