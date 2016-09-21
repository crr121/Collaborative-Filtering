# -*- coding:utf-8 -*-  
import random
import math
from operator import itemgetter
class ItemBasedCF():
	def __init__(self):
		self.train={}
		self.test={}
		self.moviecount={}
		self.Movie2MovieMatrix={}
		self.sim_movie=20
		self.rec_movie=10
		self.w={}
	'''处理数据集，分为训练集和测试集'''
	def SplitData(self):
		train_len=0
		test_len=0
		for i in open(r'C:\Users\Administrator\Desktop\ratings.dat','r').readlines():
			user,movie,rating,_=i.strip('\r\n').split('::')
			if random.random()<0.7:
				self.train.setdefault(user,{})
				self.train[user][movie]=int(rating)
				train_len+=1
			else:
				self.test.setdefault(user,{})
				self.test[user][movie]=int(rating)
				test_len+=1
		print 'train  = %s' % train_len, 'test  = %s' % test_len
		
	def ItemSimilarity(self):
		'''计算喜欢某部电影的总人数'''
		for user,movies in self.train.items():
			for movie in movies:
				if movie not in self.moviecount:
					self.moviecount[movie]=0
				self.moviecount[movie]+=1
		'''建立Movie to Movie矩阵'''
		for user , movies in self.train.items():
			for m1 in movies.keys():
				for m2 in movies.keys():
					if m1 == m2 :
						continue
					self.Movie2MovieMatrix.setdefault(m1,{})
					self.Movie2MovieMatrix[m1].setdefault(m2,0)
					self.Movie2MovieMatrix[m1][m2]+=1
		'''计算最终电影相似度矩阵w'''
		for m1,related_movie in self.Movie2MovieMatrix.items():
			for m2 , count in related_movie.items():
				self.w.setdefault(m1,{})
				self.w[m1].setdefault(m2,0)
				self.w[m1][m2]=count/math.sqrt((self.moviecount[m1])*self.moviecount[m2])
		
	'''推荐函数	'''
	def recommend(self,user):
		rank={}
		K=self.sim_movie
		N=self.rec_movie
		watched_movie=self.train[user]
		for movie , rating in watched_movie.items():
			for related_movie,count in sorted(self.w[movie].items(),key=itemgetter(1),reverse=True)[:K]:
				if related_movie in watched_movie:
					continue
				rank.setdefault(related_movie,0)
				rank[related_movie]+=count*rating
		return sorted(rank.items(),key=itemgetter(1),reverse=True)[:N]
		
if __name__=='__main__':
	user=raw_input()
	itemcf=ItemBasedCF()
	itemcf.SplitData()
	itemcf.ItemSimilarity()
	for i,sim in itemcf.recommend(user):
		print i
		
		
		
