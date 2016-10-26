#!/usr/bin/python
import requests,traceback
from bs4 import BeautifulSoup
import datetime
from datetime import date,timedelta
import json
s = requests.get("http://www.naukri.com/top-company-jobs#topJobsSection")
code = BeautifulSoup(s.text)
#print code.prettify()

bcode = code.find(id="tabs_job")
urlbyalphabet = []

for link in bcode.find_all('a'):
	urlbyalphabet.append(link.get('href'))

urlbyalphabet = urlbyalphabet[0:27]
i=0
#print len(urlbyalphabet)

###################################### url of companies ###############################################################
urlofcompanies=[]
while i < len(urlbyalphabet):
	script_url=requests.get(urlbyalphabet[i])
	info_company = BeautifulSoup(script_url.text)

	company = info_company.find(id="tabJ-A")

	for link in company.find_all('a'):
		urlofcompanies.append(link.get('href'))
	i+=1
	#print len(urlofcompanies)

#print urlofcompanies
#print len(urlofcompanies)

#print urlofcompanies[0]
#print urlofcompanies[-1]	
#######################################################################################################################
totaljobs=0
####################################################
def jobtitle(title):			
	title=title.get_text()
	title=" ".join(title.split())
	#print title
	return title
####################################################

####################################################
def experience(er):				
	er=er.get_text()
	if er =='0 Years' or er == '0 yrs':
		min_exp='0 Years'
		max_exp='Not Available'
	else:
		e=[int(exp) for exp in er.split() if exp.isdigit()]
		#min_exp = er.split(" - ",1)[0]+(' Years')
		#print exp
		min_exp=str(e[0])+(' Years')
		#max_exp = er.split(" - ",1)[1]
		max_exp=str(e[1])+(' Years')
	#print min_exp
	return (min_exp,max_exp)
	#print max_exp
####################################################

####################################################
def list_location(loc):
	location=[]
	for location_name in loc.find_all('a'):
		location_name=location_name.get_text()
		location_name=" ".join(location_name.split())
		location.append(location_name)
	#print location
	return location
####################################################		

###########################################function for job details####################################################
def jobdetails(url):
	script_job = requests.get(url)
	info_job = BeautifulSoup(script_job.text)
	type_company=0
	
	try:
		title_1 = info_job.find(itemprop="title")
		if bool(title_1) is True:	
			title_1=jobtitle(title_1)
			type_company=1
			#print title
			#print type_company
	except:
		print 'error in title'
	
	try:
		title_2 = info_job.find("h1",{"title":"jobTitleHeading"})
		if bool(title_2) is True:
			title_2=jobtitle(title_2)
			type_company=2
			#print type_company
	except:
		print 'error in title'	
	
	try:
		title_3 = info_job.find_all("table",{"class":"jobsTable"})
		if bool(title_3) is True:	
			title_3=title_3[1]
			i=0
			p = title_3.find_all('tr')
			while i<len(p):
				if title_3.find_all('tr')[i].find_all('td')[0].text.strip()=='Designation':
					title_3=title_3.find_all('tr')[i].find_all('td')[1].text
					#print title_3
					break
				i+=1
			type_company=3
			#print type_company
	except:
		print 'error in title'

	#print type_company

	#except:
	#	print 'error in title'
	'''	
	try:
		ho = info_job.find(itemprop="hiringOrganization")
		if bool(ho) is True:		
			c_name=ho.get_text()
			c_name=" ".join(c_name.split())
			print c_name
	except:
		print 'error in company name'
	'''
	try:
		org_script=requests.get(urlofcompanies[j])
		org_info=BeautifulSoup(org_script.text)
		ho=org_info.find_all(itemprop="hiringOrganization")[0]
		if bool(ho) is True:		
			c_name=ho.get_text()
			c_name=" ".join(c_name.split())
	#		print c_name
	except:
		print 'error in company name'

	url_job = url
	#print url_job

	if type_company==1:
		title=title_1
	elif type_company==2:
		title=title_2
	elif type_company==3:
		title=title_3
		#print url_job

	#print title

	if type_company == 1:			
		try:
			er = info_job.find(itemprop="experienceRequirements")
			if bool(er) is True:		
				[min_exp,max_exp]=experience(er)
		except IndexError:
			print 'error in experience'
			
		try:
			loc=info_job.find("div", { "class" : "loc"})
			if bool(loc) is True:
				location=list_location(loc)
		except:
			print 'error in location'
			
		try:
			desc = info_job.find(itemprop="description")
			if bool(desc) is True:
				desc=desc.get_text()
				desc=" ".join(desc.split())
			#	print desc
		except:
			print 'error in description'
		
		try:	
			keyskills=[]
			ks=info_job.find("div",{"class" : "ksTags"})
			if bool(ks) is True:
				for skill in ks.find_all('span'):
					skill=skill.get_text()
					skill=" ".join(skill.split())
					keyskills.append(skill)
				for skill in ks.find_all("font",{"class" : "hlite"}):
					skill=skill.get_text()
					skill=" ".join(skill.split())
					keyskills.append(skill)
			#	print keyskills
		except:
			print 'error in keyskills'

		from1= "http://www.naukri.com/"
		#print from1

		try:
			industry=[]
			it=info_job.find(itemprop="industry")
			if bool(it) is True:
				for it_name in it.find_all('a'):
					it_name=it_name.get_text()
					it_name=" ".join(it_name.split())
					industry.append(it_name)
		#		print industry
		except:
			print 'error in industry'

		try:
			job_function=[]
			jf=info_job.find(itemprop="occupationalCategory")
			if bool(jf) is True:	
				for jf_name in jf.find_all('a'):
					jf_name=jf_name.get_text()
					jf_name=" ".join(jf_name.split())
					job_function.append(jf_name)
		#		print job_function
		except:
			print 'error in functionl area'

		try:
			education=[]
			ec=info_job.find(itemprop="educationRequirements")
			if bool(ec) is True:
				for degree in ec.find_all('em'):
				     a = degree.get_text()
				     b =ec.find('span')
				     b = b.get_text()
				     c = str(a)+str(b)
				     c = " ".join(c.split())
			 	     education.append(c)
		#	 	print education
		except:
			print 'error in education'

		try:
		 	info_day = info_job.find("div",{"class":"sumFoot"})	
		 	if bool(info_day) is True:
		 		i=0
				while i<4:
					dd = info_day.find_all('span')[i]
					nday=dd.get_text()
					if nday[0:7] == 'Posted ':
					 	if nday=='Posted Just Now' or nday=='Posted Today' or nday =='Posted Few Hours Ago':
					 		posted_date=date.today()
					 		posted_date=str(posted_date)
		#			 		print posted_date
							break
						else:
						 	nday=nday.split("Posted ",1)[1].split(" ",1)[0]
						 	d=int(nday)
						 	posted_date=date.today()-timedelta(days=d)
						 	posted_date=posted_date.strftime("%d-%m-%Y")
						 	posted_date=str(posted_date)
		#				 	print posted_date
						 	break
					i+=1
		except:
			print 'error in posted date'	
		
	elif type_company == 2:

		try:
			er = info_job.find_all("span", { "class" : "fl"})[3]
			if bool(er) is True:
				[min_exp,max_exp]=experience(er)
		except IndexError:
			print 'error in experience'

		try:
			loc=info_job.find("span",{"class":"fl disc-li"})
			if bool(loc) is True:	
				location=list_location(loc)
		except:
			print 'error in location'

		try:
			desc = info_job.find("div",{"class":"f14 lh18 alignJ disc-li"})
			if bool(desc) is True:
				desc=desc.get_text()
				desc=" ".join(desc.split())
				desc = desc.split("Salary",1)[0]
		#		print desc
		except:
			print 'error in description'
	
		try:
			keyskills=[]
			ks = info_job.find_all("a",{"class":"tag"})
			if bool(ks) is True:
				i=0
				while i <len(ks):
					skill=ks[i].get_text()
					#skill=" ".join(skill.split())
					keyskills.append(skill)
					i+=1
		#		print keyskills
		except:
			print 'error in keyskills'

		from1= "http://www.naukri.com/"
		#print from1

		try:
			industry=[]
			it=info_job.find("div",{"class":"f14 lh18 alignJ disc-li"})
			if bool(it) is True:
				it=it.get_text()
				it=it.split("Industry:",1)[1].split("Functional Area:",1)[0]
				it=" ".join(it.split())
				industry=it.split(" / ")
		#		print industry
		except:
			print 'error in industry'

		try:
			job_function=[]
			jf=info_job.find("div",{"class":"f14 lh18 alignJ disc-li"})
			if bool(jf) is True:
				jf=jf.get_text()
				jf=jf.split("Functional Area:",1)[1].split("Role Category:",1)[0]
				jf=" ".join(jf.split())
				job_function=it.split(", ")
		#		print job_function
		except:
			print 'error in functional area'	

		try:
			education=[]
			ec = info_job.find("div",{"class":"f14 lh18 disc-li"})
			if bool(ec) is True:
				ec=ec.get_text()
				ec=ec.replace('Education:','').replace('UG','@UG',1).replace('PG','@PG',1).replace('Doctorate','@Doctorate',1)
				ec=" ".join(ec.split())
				education=ec.split('@')
				if education[0]=='':
					education.pop(0)
		#		print education
		except:
			print 'error in education'	

		try:
			info_day=info_job.find(id="postDateInfo")
			if bool(info_day) is True:
				nday=info_day.get_text()
				if nday=='Posted: Just Now' or nday=='Posted: Today' or nday =='Posted: Few Hours Ago':
					posted_date=date.today()
					posted_date=str(posted_date)
		#			print posted_date
				else:
					e=[int(exp) for exp in nday.split() if exp.isdigit()]
					posted_date=date.today()-timedelta(days=e[0])
					posted_date=posted_date.strftime("%d-%m-%Y")
					posted_date=str(posted_date)
		#			print posted_date
		except:
			print 'error in posted date'

	elif type_company == 3:
		#experience
		try:
			er = info_job.find_all("table",{"class":"jobsTable"})[1]
			if bool(er) is True:
				i=0
				p = er.find_all('tr')
				while i<len(p):
					if er.find_all('tr')[i].find_all('td')[0].text.strip()=='Experience':
						er=er.find_all('tr')[i].find_all('td')[1].text
						break
					i+=1
				if er.strip() =='0 Years' or er.strip() == '0 yrs':
					min_exp='0 Years'
					max_exp='Not Available'
				else:	
					a=[int(exp) for exp in er.split() if exp.isdigit()]
					min_exp =str(a[0])+(' Years')
					#print min_exp
					max_exp=str(a[1])+(' Years')
					#print max_exp 
		except:
			print 'error in experience'
			
		#location
		try:
			location=[]
			loc = info_job.find_all("table",{"class":"jobsTable"})[1]
			if bool(loc) is True:
				i=0
				p = loc.find_all('tr')
				while i<len(p):
					if loc.find_all('tr')[i].find_all('td')[0].text.strip()=='Location':
						loc=loc.find_all('tr')[i].find_all('td')[1].text
						break
					i+=1	
				loc=" ".join(loc.split())
				location.append(loc)
				'''
				ln=loc.find_all('td',{'class':'detailJob'})
				l=0
				while l<len(ln):
					location_name=ln[l]
					location_name=" ".join(location_name.split())
					location.append(location_name)
					l+=1
				'''
		#		print location		
		except:
			print 'error in location'
		
		#Description
		try:
			desc = info_job.find_all("table",{"class":"jobsTable"})[1]
			if bool(desc) is True:
				i=0
				p = desc.find_all('tr')
				while i<len(p):
					if desc.find_all('tr')[i].find_all('td')[0].text.strip()=='Job Description':
						desc=desc.find_all('tr')[i].find_all('td')[1].text
						break
					i+=1
				desc=" ".join(desc.split())
		#		print desc
		except:
			print 'error in Description'

		#keyskills
		try:
			keyskills=[]
			ks = info_job.find_all("table",{"class":"jobsTable"})[1]
			if bool(ks) is True:
				i=0
				p = ks.find_all('tr')
				while i<len(p):
					if ks.find_all('tr')[i].find_all('td')[0].text.strip()=='Keywords':
						ks=ks.find_all('tr')[i].find_all('td')[1]
						break
					i+=1
				a = ks.get_text()
				for skill in ks.find_all('a'):
					skill = skill.get_text()
					skill=" ".join(skill.split())
					keyskills.append(skill)
				l=0
				while l<len(keyskills):
					a=a.replace(keyskills[l],'')
					l+=1
				a=" ".join(a.split())
				keyskills.append(a)
				#print keyskills
		except:
			print 'error in keyskill'		
		
		#from1
		from1= "http://www.naukri.com/"
		#print from1
		
		#industry
		try:
			industry=[]
			it=info_job.find_all("table",{"class":"jobsTable"})[1]
			if bool(it) is True:
				i=0
				p = it.find_all('tr')
				while i<len(p):
					if it.find_all('tr')[i].find_all('td')[0].text.strip()=='Industry Type':
						it=it.find_all('tr')[i].find_all('td')[1].text
						break
					i+=1
				it=it.split("/ ")
				industry = [x.strip(' ') for x in it]
		#		print industry
		except:
			print 'error in industry'		

		#job_function
		try:
			job_function=[]
			jf=info_job.find_all("table",{"class":"jobsTable"})[1]
			if bool(jf) is True:
				i=0
				p = jf.find_all('tr')
				while i<len(p):
					if jf.find_all('tr')[i].find_all('td')[0].text.strip()=='Functional Area':
						jf=jf.find_all('tr')[i].find_all('td')[1].text
						break
					i+=1
				job_function=jf.split(", ")
			#	print job_function
		except:
			print 'error in functional area'		

		#education
		try:
			education=[]
			ec=info_job.find_all("table",{"class":"jobsTable"})[1]
			if bool(ec) is True:
				i=0
				p = ec.find_all('tr')
				while i<len(p):
					if ec.find_all('tr')[i].find_all('td')[0].text.strip()=='Education':
						ec=ec.find_all('tr')[i].find_all('td')[1]
						break
					i+=1
				for degree in ec.find_all('em'):
				     a = degree.get_text()
				     b =ec.find('span')
				     b = b.get_text()
				     c = str(a)+str(b)
				     c = " ".join(c.split())
			 	     education.append(c)
			 #	print education
		except:
			print 'error in education'		

		#posted_date
		try:
			info_day=info_job.find_all("table",{"class":"jobsTable"})[1]
			if bool(info_day) is True:
				i=0
				p = info_day.find_all('tr')
				while i<len(p):
					if info_day.find_all('tr')[i].find_all('td')[0].text.strip()=='Job Posted':
						info_day=info_day.find_all('tr')[i].find_all('td')[1].text
						break
					i+=1
				posted_date=info_day[0:11]
				posted_date=str(posted_date)
				#print posted_date
		except:
			print 'error in Posted date'	
	else:
		print 'new type of company'

	data=json.dumps({'Title':title,'Comapny Name':c_name,'Page Link':url_job,'Minimum Experience':min_exp,'Maximum Experience':max_exp,'Location':location,'Description':desc,'Key Skills':keyskills,'Industry':industry,'Website':from1,'Functional Area':job_function,'Education':education,'Posted Date':posted_date},indent=4)
	print data
	#data=json.dumps([title,c_name,url_job,min_exp,max_exp,location,desc,keyskills,industry,from1,job_function,education,posted_date],indent=1)
	# data

	
	#with open('data.txt', 'a') as outfile:
	#	json.dump(data,outfile,sort_keys=True,separators=(',', ':'))
	#	json.dump('													',outfile,sort_keys=True,separators=(',', ':'))
	
	print '----------------------------------------------------'		
#######################################################################################################################

#####################################################get details of more another pages of company #####################
def getdetailsofanotherpages(url_otherpage):
	script_otherpage = requests.get(url_otherpage)
	info_otherpage = BeautifulSoup(script_otherpage.text)
	njobs_otherpage=info_otherpage.find_all(itemtype="http://schema.org/JobPosting")
	#print len(njobs_otherpage)
	#totaljobs+=len(njobs_otherpage)
	n=1
	while n<=len(njobs_otherpage):
		urlofotherjobs=info_otherpage.find(count=n)
		url=urlofotherjobs.get('href')
		jobdetails(url)
		n+=1
	try:		
		mydivs = info_otherpage.find_all("div", { "class" : "pagination"})[0]
		#print mydivs
		pagelink=mydivs.find_all('a')[1]
		url_otherpage=pagelink.get('href')
		print '----------------------------------------------------'
		#print url_otherpage
		getdetailsofanotherpages(url_otherpage)
	except:
		print 'No more pages found'

j=0
companyjobs=0
error_company=[]
#p = urlofcompanies.index("http://www.naukri.com/bptp-jobs-careers-116648")
#j=p
#'''len(urlofcompanies)''' 
while j<len(urlofcompanies):
	try:
		#print urlofcompanies[j]
		script_company = requests.get(urlofcompanies[j])
		info = BeautifulSoup(script_company.text)
		string_jobs = info.find("span",{ "class" : "cnt"})
		if bool(string_jobs) is True:
			title_string_jobs=string_jobs.attrs['title']
			cjobs=title_string_jobs.split("of ",1)[1]
			companyjobs=int(cjobs)
		else:
			error_company.append(urlofcompanies[j])
		
		njobs=info.find_all(itemtype="http://schema.org/JobPosting")
		print len(njobs)
		#totaljobs+=len(njobs)
		k=1
		while k<=len(njobs):
			urlofjob=info.find(count=k)
			url=urlofjob.get('href')
			jobdetails(url)
			k+=1	
		try:
			mydivs = info.find_all("div", { "class" : "pagination"})[0]
			#print mydivs
			pagelink=mydivs.find_all('a')[0]
			url_otherpage=pagelink.get('href')
			print '----------------------------------------------------'
			#print url_otherpage
			getdetailsofanotherpages(url_otherpage)
		except:
			print 'No other pages - not more than 20 jobs '
	except Exception,err:
		print traceback.format_exc()	
	#jobdetails("http://www.naukri.com/job-listings-Chinese-Fastfood-Restaurant-Assistant-Manager-YiChiLai-Restaurants-North-India-Pvt-Ltd-Gurgaon-3-to-6-years-010616003556?src=jobsearchDesk&sid=14671753467099&xp=1")

	print(j,companyjobs)
	companyjobs=0
	j+=1

print error_company
j=0