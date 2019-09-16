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

vector<string> prov;
map<string, set<string> > res;

void prov_init()
{
    prov.push_back("../pred/00-BeiJing");
    prov.push_back("../pred/01-HuBei");
    prov.push_back("../pred/02-HeiLongJiang");
    prov.push_back("../pred/03-LiaoNing");
}

int main()
{
    prov_init();
    for(vector<string>::const_iterator it=prov.begin();it!=prov.end();it++)
    {
        ifstream inf((*it).c_str());
        if(!inf)
        {
            cout<<"failed in opening "<<*it<<endl;
            continue;
        }
        while(1)
        {
            string name,tmp;
            inf>>name>>tmp>>tmp; //score #
            if(inf.eof())
                break;
            while(1)
            {
                string tag;
                inf>>tag;
                if(tag=="#")
                    break;
                res[name].insert(tag);
            }
        }
    }
    for(map<string, set<string> >::const_iterator it=res.begin();it!=res.end();it++)
    {
	ofstream ouf(("data/"+it->first).c_str());
        for(set<string>::const_iterator it2=it->second.begin();it2!=it->second.end();it2++)
        {
            ouf<<*it2<<endl;
        }
    }

}
