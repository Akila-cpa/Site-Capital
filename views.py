from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.db import connection
from django.contrib import messages






def modifier(request,age,nsous):

    query1=f""" UPDATE spouvcapb SET eta='HH' WHERE age='{age}' and nsous='{nsous}'  """
    with connection.cursor() as curso: 
            curso.execute(query1)
            curso.commit()
            curso.close()
    #messages.success(request, "Votre action a été effectuée avec succès !")
    #return redirect( 'index')
    return JsonResponse()





def libelle_segment(seg):
    code='095' 
    seg='095'+seg
   # seg=f"{code}{seg}"
        
    query=f""" select  cacc,lib4,lib1,lib2,lib3,lib5,mnt1,mnt2,mnt3 from cpa_bknom where ctab='790' and  cacc[1,4]='{seg}'
                      """
    with connection.cursor() as cursor: 
        cursor.execute(query)
        result = cursor.fetchone()[2]

    return result

def segments(request):

    segs = ["A", "B", "C","D","E","F"]
    actions_par_seg = {}
     
    with connection.cursor() as cursor:
        for type_action in segs:
            query=f"""
                SELECT age,nsous,seg,cli,nba,mon 
                FROM spouvcapb
                WHERE eta ='ED' and seg ='{type_action}' order by age,seg """ 
            
            cursor.execute(query)
           
             # Stocker les résultats sous forme de dictionnaires
            actions = [ {"age": row[0], "nsous": row[1], "seg": row[2],  "cli": row[3], "nba": row[4], "mon": row[5]}    
                        for row in cursor.fetchall()
                    ]
                    # Ajouter les options au type correspondant
             

            if actions:
                libelle = libelle_segment(type_action)
                se =  type_action
                # calcul des totaux
                total_cli = len(set(action["cli"] for action in actions))#len(set(action["cli"]) for action in actions)
                total_nba = sum(int(action["nba"] )for action in actions)
                total_mon = sum(float(action["mon"] )for action in actions)
                total_agences = len(set(action["age"] for action in actions))  # Nombre unique d'agences

                actions_par_seg[type_action] = {
                    "libelle": libelle,
                    "actions": actions,
                    "total_cli": total_cli,
                    "total_nba": total_nba,
                    "total_mon": total_mon,
                    "total_agences": total_agences,
                    "se" : se 
                }
                
                          
    return render(request, 'segments.html', { 'actions_par_seg': actions_par_seg })



def liste_actions(request):
    query=f"""
            SELECT age,seg FROM spouvcapb  where eta<>'HH' and age<>'''' and seg<>'''' group by age,seg order by  seg,age desc
            """
    with connection.cursor() as cursor:

        cursor.execute(query)
        liste=cursor.fetchall()
    
    #print(liste)
    liste1 = [ { "Agence": row[0], "Segment": row[1]}  for row in liste ]
    
    return JsonResponse(liste1, safe=False)


def index(request):

    query="""
            SELECT distinct(seg) FROM spouvcapb order by seg
            """
    
    with connection.cursor() as cursor:
        cursor.execute(query)
        segments=cursor.fetchall()

    query="""
            SELECT age,nsous,seg,cli,nba,mon  FROM spouvcapb where eta <>'HH'group by age,nsous,seg,cli,nba,mon 
            order by age,nsous,seg
            """
    
    with connection.cursor() as cursor:
        cursor.execute(query)
        actions = cursor.fetchall()
    print(actions)    

    
    context = { 'actions' : actions ,'segments' : segments } 
    
    return render(request, 'home.html', context)

