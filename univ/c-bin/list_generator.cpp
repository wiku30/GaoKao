#include "iostream"
#include "fstream"
#include "string"
#include "map"
#include "cstdlib"
#include "vector"
#include "iomanip"
#include "queue"
#include "cstring"
#include "set"
using namespace std;

typedef map<int, map<int, float> > lst;
typedef map<int, float> std_points;

struct info
{
    std_points stdpt;
    set<string> tags;
};

typedef map<string, info> dataset;

map<int,string> zone;

void map_init()
{
    zone[0]="BeiJing";
    zone[1]="HuBei";
    zone[2]="HeiLongJiang";
    zone[3]="LiaoNing";
}

struct univ
{
    string name;
    set<string> attr;
    int pred;
    univ(string a,int b):name(a),pred(b){}
};

typedef priority_queue<univ> ulist;

bool operator <(univ a,univ b)
{
    return a.pred<b.pred;
}


void get_list(lst& res, int begin_year, int end_year, int area)
{
    res.clear();
    ifstream inf;
    map<int, map<int, float> > conv;
    for(int yr=begin_year ; yr<end_year ; yr++)
    {
        char path[]="../std/00-2010";
        path[7]='0'+area/10;
        path[8]='0'+area%10;
        path[13]='0'+(yr-2010);
        cout<<path<<endl;
        inf.open(path);
        if(!inf)
            continue;
        while(1)
        {
            int orgpt;
            float stdpt;
            inf>>orgpt;
            if(inf.eof())
                break;
            inf>>stdpt;
            res[yr][orgpt]=stdpt;
        }
        inf.close();
    }
}

int get_score(float stdpt, lst& conv, int year, int mi, int ma)
{
    if(ma-mi<=1)
        return mi;
    int mid=(mi+ma)/2;
    if(conv[year][mid]>stdpt)
        return get_score(stdpt,conv,year,mi,mid);
    else
        return get_score(stdpt,conv,year,mid,ma);
}

ulist get_univ(int area, dataset& data, lst& conv, int begin_year, int end_year)
{
    ulist res;
    data.clear();
    char path[30]="../univ-data/res-00";

    path[17]='0'+area/10;
    path[18]='0'+area%10;


    ifstream inf(path);
    if(!inf)
        return res;

    while(1)
    {
        int group, year, orgpt;
        string name, place, type, tmp;
        float stdpt;
        inf>>group;
        if(group!=1) //only consider first-group universities
            break;
        inf>>name>>year>>type>>orgpt>>tmp; //tmp="#"
        while(1)
        {
            inf>>tmp;
            if(tmp=="#")
                break;
            data[name].tags.insert(tmp);
        }
        stdpt=conv[year][orgpt];
        if(conv.find(year)==conv.end())
            continue;
        if(type=="S") //only consider science type.
        {
            data[name].stdpt[year]=stdpt;
        }

    }
    cout<<data.size()<<endl;
    dataset::iterator it;

    for(it=data.begin();it!=data.end();it++)
    {
        try
        {
            set<string> tag;
            float pred=0;
            int num=0;
            for(int k=begin_year;k<end_year;k++)
            {
                if(it->second.stdpt.find(k)!=it->second.stdpt.end() && it->second.stdpt[k]>1)
                {
                    num++;
                    pred+=it->second.stdpt[k];
                    if(tag.empty())
                    {
                        tag=it->second.tags;
                    }

                }
            }
            if(!num)
                throw(1);
            pred/=num;
            univ tmp(it->first,get_score(pred,conv,2016,500,720));
            tmp.attr=tag;
            res.push(tmp);
        }
        catch(int)
        {
            continue;
        }
    }
    return res;
    inf.close();
}

void output(int area, ulist res)
{
    char output_path[30]="../pred/00-";
    output_path[8]='0'+area/10;
    output_path[9]='0'+area%10;
    strcat(output_path,zone[area].c_str());
    cout<<output_path;
    ofstream ouf(output_path);

    while(res.size())
    {
        univ tmp=res.top();
        ouf<<tmp.name<<" "<<tmp.pred<<"    # ";
        for(set<string>::iterator i=tmp.attr.begin(); i!=tmp.attr.end(); i++)
        {
            ouf<<*i<<" ";
        }
        ouf<<"#"<<endl;
        res.pop();
    }
    ouf.close();
}

int main()
{
    lst conv;
    dataset data;
    map_init();
    int x;
    cout<<"Enter num:"<<endl;
    cin>>x;
    for(int i=0;i<x;i++)
    {
        get_list(conv,2013,2017,i);
        output(i,get_univ(i,data,conv,2013,2016));
    }

}
