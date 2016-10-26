#!/usr/bin/python
import requests,traceback
from bs4 import BeautifulSoup
import json
#l=0,
i=0
website_url='http://www.careerbuilder.co.in/intl/jobseeker/jobs/jrp.aspx'
s = requests.get(website_url)
data = BeautifulSoup(s.text)

urlofcity=[]
c = data.find(id='_ctl1_TreeNavigator2_pnlToggleAll')
if bool(c):
	n = c.find_all('div',{'class':'facet'})
	if bool(n):
		while i<len(n):
			try:
				a=n[i]
				z = a.find('span',{'class','newFacetLink'})
				x=z.get('data')
				link= "?".join((website_url,x))
				urlofcity.append(link)
			except Exception,err:
				print traceback.format_exc()
			i+=1

print len(urlofcity)
##############################################################
def jobdetails(url):
	script_job=requests.get(url)
	info_job=BeautifulSoup(script_job.text)
	print '--------------------------------------------------'
	try:
		tag=info_job.find(id='h1JobTitle').find(id='JobDetails_ucJobDetails_litTitle')
		if bool(tag):
			title=tag.text.strip().split(' | ',1)[0]
			location=tag.text.strip().split(' | ',1)[1]
			#print title
			#print location
	except Exception,err:
		print traceback.format_exc()

	try:
		ho=info_job.find('h2',{'class':'companyInfoLink'})
		if bool(ho):
			c_name=ho.text.strip()
			#print c_name
	except Exception, err:
		print traceback.format_exc()

	try:
		desc=info_job.find(id='JobDetails_ucJobDetails_litDescription')
		if bool(desc):
			desc = ' '.join(desc.text.split())
			#print desc
	except Exception, err:
		print traceback.format_exc()

	url_job = url
	#print url_job
	
	try:
		ex=info_job.find(id='experience')
		if bool(ex):
			ex=ex.next_sibling.next_element.text.strip()
			if ex=='Not Specified':
				min_exp='Not Available'
				max_exp='Not Available'
			else:
				e=[int(exp) for exp in ex.split() if exp.isdigit()]
				min_exp=str(e[0])+(' Years')
				max_exp=str(e[1])+(' Years')
			#print min_exp
			#print max_exp
	except Exception,err:
		print traceback.format_exc()

	try:
		ed=info_job.find(id='education')
		if bool(ed):
			education=ed.next_sibling.next_element.text.strip()
			#print education
		else:
			education=''
	except Exception,err:
		print traceback.format_exc()

	from1= "http://www.careerbuilder.co.in/"
#	print from1
	
	try:
		pd=info_job.find(id='JobDetails_ucJobDetails_litPostedDate')
		if bool(pd):
			posted_date=pd.text.strip()
			#print posted_date
	except Exception,err:
		print traceback.format_exc()

	try:
		industry=[]
		it=info_job.find('div',{'class':'SimilarJobsIndustries clearfix'})
		if bool(it):
			for link in it.find_all('a'):
				it_name=link.get_text().replace(' Jobs','').strip()
				industry.append(it_name)
		#print industry
	except Exception,err:
		print traceback.format_exc()
	
	try:
		keyskills=[]
		ks = info_job.find(id='JobDetails_ucJobDetails_litRequirements')
		if bool(ks):
			ks=ks.text
			a=ks.find('Key Skill')
			if a != -1:
				keyskills=ks.split('Key Skill: ',1)[1].split('Company',1)[0].strip().split('\r',1)[0].split(' / ')
				#print keyskills
			else:
				keyskills=[]
	except :
		keyskills=[]
		#print traceback.format_exc()

	job_function=[]

	data=json.dumps({'Title':title,'Comapny Name':c_name,'Page Link':url_job,'Minimum Experience':min_exp,'Maximum Experience':max_exp,'Location':location,'Description':desc,'Key Skills':keyskills,'Industry':industry,'Website':from1,'Functional Area':job_function,'Education':education,'Posted Date':posted_date},indent=4)
	print data
	#data=json.dumps([title,c_name,url_job,min_exp,max_exp,location,desc,keyskills,industry,from1,education,posted_date],indent=1)
	#print data
	
##############################################################
def detailsofpage(link):
	print link
	script_page = requests.get(link)
	info_page=BeautifulSoup(script_page.text)

	p =info_page.find(id="_ctl0_pnDataList")
	list_job=p.find_all('tr')
	remove_list_job=[0,5]
	final_list_job=[k for l, k in enumerate(list_job) if l not in remove_list_job]
	final_list_job.pop(-1)
	n=0
	while n<len(final_list_job):
		a=final_list_job[n]
		url = a.find_all('td')[1].find_all('h2')[0].find('a').get('href')
		jobdetails(url)
		n+=1

	try:
		link_nextpage=p.find_all('tr')[-1].find(id='paginationBottom').find_all('a')[-1].get('href')
		if bool(link_nextpage):
			detailsofpage(link_nextpage)
		else:
			print 'no other pages'
	except Exception, err:
		traceback.format_exc()

##############################################################	
##############################################################
j=0
while j<len(urlofcity):
	try:
		url_firstpage=urlofcity[j]
		detailsofpage(url_firstpage)
	except traceback,err:
		traceback.format_exc()

	j+=1