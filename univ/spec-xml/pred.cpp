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

#define HTML 1

#if HTML
#define br "<br>\n"
#else
#define br "\n"
#endif

using namespace std;

typedef map<int, map<int, float> > lst;
typedef map<int, float> std_points;

string root_path;

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

struct unit
{
    string name;
    int pred;
    int suf_data; //0:nothing 1:insufficient 2:sufficient
    unit(string _1, int _2, int _3):name(_1),pred(_2),suf_data(_3){}
    set<string> tags;
};

void output(const unit& x)
{
    cout<<"<h2>"<<x.name<<"</h2>预估线：";
    switch(x.suf_data)
    {
    case 0:
        cout<<"<font color=grey>不详</font>"<<br;
        break;
    case 1:
        cout<<"<font color=grey>"<<x.pred<<"*</font>"<<br;
        break;
    case 2:
        cout<<"<font color=blue>"<<x.pred<<"</font>"<<br;
    }
    if (x.tags.size())  cout<<"标签：";
    for(set<string>::iterator i=x.tags.begin();i!=x.tags.end();i++)
    {
        cout<<*i<<" ";
    }
    cout<<br;
}

void input_pat(vector<vector<string> >& pat, int argc, char** argv)
{
    int cursor=5;
    while(1)
    {
        string str;
        vector<string> tmp;
        while(1)
        {

            str=argv[cursor];
            cursor++;

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

bool check(const vector<vector<string> >& pat, const set<string>& cand)
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
            if(cand.find(*i2)!=cand.end())
                flag=1;
        }
        if(!flag)
            return 0;
    }
    return 1;
}

bool operator <(unit a,unit b)
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
        inf.open((root_path+path).c_str());
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

void get_tags(set<string>& tags,string univ)
{
    string univ_path=root_path+"../tags/data/"+univ;
    ifstream inf(univ_path.c_str());
    if(!inf)
    {
        return;
    }

    while(1)
    {
        string tag;
        inf>>tag;
        //cout<<univ_path<<endl;
        if(inf.eof())
            break;
        //cout<<tag<<endl;
        tags.insert(tag);
    }
}

void query(lst& conv, bool isuniv , string name, string path, int begin_year, int end_year, int argc, char** argv, int query_score=0, int min_num=5)
{
    ifstream inf(path.c_str());
    int type,year,score;
    string univ,spec,_score;
    map<string, map<int, int > >  data;
    priority_queue<unit> pq;
    vector<vector<string> > pat;

    bool found=0;
    int max_score=query_score+8;
    int min_score=query_score-20;
    if(!isuniv) input_pat(pat,argc,argv);
    while(1)
    {

        inf>>type;
        if(inf.eof() || type!=1)
            break;
        inf>>univ>>spec>>year>>_score;
        score=atoi(_score.c_str());
        if(score<100)
            continue;
        if(isuniv)
        {
            min_num=9999999; //unlimited
            max_score=9999;
            min_score=1;
            if(name==univ && year>=begin_year && year<end_year)
            {
                data[spec][year]=score;
            }
        }
        else
        {



            if(spec.find(name)!=-1 && year>=begin_year && year<end_year)
            {
                set<string> tags;
                get_tags(tags,univ);

                if(check(pat,tags))
                    data[univ+" "+spec][year]=score;

            }
        }
        //cout<<name<<" "<<type<<endl;
    }
    bool insuf=0;
    for(map<string, map<int, int> >::iterator i1=data.begin();i1!=data.end();i1++)
    {
        int num=0;
        float avg=0;
        for(int y=begin_year;y<end_year;y++)
        {
            if(i1->second.find(y)!=i1->second.end() && conv[y][data[i1->first][y]]>40)
            {
                num++;
                avg+=conv[y][data[i1->first][y]];
            }

        }
        if(num)avg/=num;
        unit un(i1->first,get_score(avg,conv,end_year,500,720),2);

        if (!isuniv)
        {
            string univ_name=i1->first;
            univ_name.resize(i1->first.find(" "));
            get_tags(un.tags,univ_name);
        }
        if(num*2>=end_year-begin_year)
        {
            un.suf_data=2;
        }
        else if(num)
        {
            un.suf_data=1;
            insuf=1;
        }
        else
        {
            un.suf_data=0;
        }
        pq.push(un);
    }
    if(!pq.size())
    {
        cout<<"<h1>暂无该院校专业分数信息！</h1>";
    }

    while(pq.size())
    {
        const unit& t=pq.top();
        if(t.pred<=max_score)
            if(t.pred>=min_score || min_num>0)
            {
                output(t);
                min_num--;
            }
            else
            {
                break;
            }

        pq.pop();
    }
    if(insuf)
    {
        cout<<"<br><font color=grey>*:数据不足，可能有较大偏差。</font>"<<endl;
    }
}

int main(int argc, char** argv) // ./pred 1 -u 清华大学
                                // ./pred 1 -s 计算机 640 (tags) #
{
    root_path=argv[0];
    root_path.resize(root_path.size()-4);
    if(argc<3)
        return 99999;
    int prov_no=atoi(argv[1]);
    lst conv;
    get_list(conv,2013,2017,prov_no);
    string path="processed/00";
    path[10]=prov_no/10+'0';
    path[11]=prov_no%10+'0';
    if(string("-u")==argv[2])
        query(conv,1,argv[3],(root_path+path),2013,2016,argc,argv,0);
    else if(string("-s")==argv[2])
    {
        query(conv,0,argv[3],(root_path+path),2013,2016,argc, argv,atoi(argv[4]));
    }

}
