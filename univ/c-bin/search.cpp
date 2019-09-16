#include <iostream>
#include <string>
#include <set>
#include <vector>
#include <fstream>
#include <cstdlib>

using namespace std;

bool HTML=0;

int province=0;

struct univ
{
    string name;
    int pred;
    set<string> tags;
};

istream& operator >>(istream& inf, univ &u)
{
    string tmp;
    inf>>u.name>>u.pred>>tmp; //tmp=="#"
    if(inf.eof())
        return inf;
    while(1)
    {
        inf>>tmp;
        if(tmp=="#")
            return inf;
        u.tags.insert(tmp);
    }
}

ostream& operator <<(ostream& ouf, const univ &u)
{
    if(!HTML)
        ouf<<u.name<<" "<<u.pred<<"    # ";
    else
    {
        ouf<<"<h1>"<<u.name<<"</h1>"<<endl;
        ouf<<"预测平均分：<font color=blue>"<<u.pred<<"</font><br>标签："<<endl;
    }

    for(set<string>::iterator it=u.tags.begin();it!=u.tags.end();it++)
    {
        ouf<<*it<<" ";
    }
    if(!HTML)
        ouf<<"#"<<endl;
    else
        ouf<<"<br>"<<endl;
        ouf<<"<a href=/spec.php?univ="<<u.name<<"&prov="<<province<<"&type=-u>专业信息</a><br>"<<endl;
    return ouf;
}

void getdata(vector<univ>& res, const char* path)
{
    ifstream inf(path);
    if(!inf)
        return;
    while(1)
    {
        univ tmp;
        inf>>tmp;
        if(inf.eof())
            return;
        res.push_back(tmp);
    }
    inf.close();
}

ostream& operator << (ostream& os, const vector<univ>& un)
{
    for(unsigned i=0; i<un.size();i++)
    {
        os<<un[i];
    }
    if(!un.size())
    {
        cout<<"<h1>未找到符合要求的院校！</h1>";
    }

    return os;
}

bool check(const vector<vector<string> >& pat, const univ& cand)
//pat: conjunctive normal form
{
    if(!pat.size())
        return 1;
    for(vector<vector<string> >::const_iterator i1=pat.begin();i1!=pat.end();i1++)
    {
        int flag=0;
        if(!i1->size())
            flag=1;
        for(vector<string>::const_iterator i2=i1->begin();i2!=i1->end();i2++)
        {
            if(cand.tags.find(*i2)!=cand.tags.end())
                flag=1;
        }
        if(!flag)
            return 0;
    }
    return 1;
}

void filter(vector<univ>& res, const vector<univ>& src, int score, const vector<vector<string> >& pat, int minnum=7, int upbound=5, int lobound=10)
{
    for(vector<univ>::const_iterator it=src.begin();it!=src.end();it++)
    {
        if(it->pred>score+upbound) //descending order
        {
            continue;
        }
        if(check(pat,*it))
        {
            minnum--;
            res.push_back(*it);
        }
        if(minnum<=0 && it->pred<score-lobound)
            return;
    }
}

void input_pat(vector<vector<string> >& pat, int argc, char** argv)
{
    if(argc==1)
        cout<<"Enter filter conditions, finishing with a space and #."<<endl;
    int cursor=3;
    while(1)
    {
        string str;
        vector<string> tmp;
        while(1)
        {
            if(argc==1)
                cin>>str;
            else
            {
                str=argv[cursor];
                cursor++;
            }
            if(str == "#" || str == "and")
            {
                break;
            }
            tmp.push_back(str);
        }
        pat.push_back(tmp);
        if(str=="#")
            return;
    }
}

int main(int argc, char** argv)
{
//argv[1]: province
//argv[2]: score
    if(argc==1)
        cout<<"Enter province symbol: (like HuBei)"<<endl;
    else
        HTML=1;
    string location(argv[0]);
    location.resize(location.size()-6);
    string prefix("../pred/00-");
    string suffix,path;

    if(argc==1)
        cin>>suffix;
    else
        suffix=argv[1];
    int i=0;
    for(i=0; i<=99; i++)
    {
        prefix[8]=i/10+'0';
        prefix[9]=i%10+'0';
        path=location+prefix+suffix;
        if(ifstream(path.c_str()))
            break;
    }
    if(i==100)
    {
        cout<<"Province not found!"<<endl;
        return 0;
    }
    province=i;
    if(argc==1)
    {
        cout<<"Enter your score:"<<endl;
        cin>>i;
    }
    else
        i=atoi(argv[2]);
    vector<vector<string> > pat;
    input_pat(pat,argc,argv);
    vector<univ> data,res;
    getdata(data, path.c_str());
    filter(res,data,i,pat);
    cout<<res;

    return 0;
}
