# -*- coding:utf-8 -*-  
import random
import math
from operator import itemgetter
class UserBasedCF():
	def __init__(self):
		self.train={}
		self.test={}
		self.UserSimilarityMatrix={}
		self.Moive2UserMatrix={}
		self.sim_movie=20
		self.rec_movie=10
		self.w={}
	'''处理数据集，分为训练集和测试集'''
	def SplitData(self):
		train_len=0
		test_len=0
		for i in open(r'C:\Users\Administrator\Desktop\ml-1m\ratings.dat','r').readlines():
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
		
	def UserSimilarity(self):
		'''建立Movie to users矩阵'''
		for user , movies in self.train.items():
			for i in movies.keys():
				if i not in self.Moive2UserMatrix:
					self.Moive2UserMatrix[i]=set()
			self.Moive2UserMatrix[i].add(user)
		'''	建立用户相似度矩阵'''
		for movie , users in self.Moive2UserMatrix.items():
			for u1 in users:
				for u2 in users:
					if u1 == u2 :
						continue
					self.UserSimilarityMatrix.setdefault(u1,{})
					self.UserSimilarityMatrix[u1].setdefault(u2,0)
					self.UserSimilarityMatrix[u1][u2]+=1
		'''计算最终相似度矩阵w'''
		for u,related_user in self.UserSimilarityMatrix.items():
			for v , count in related_user.items():
				self.w.setdefault(u,{})
				self.w[u].setdefault(v,0)
				self.w[u][v]=count/math.sqrt(len(self.train[u])*len(self.train[v]))
		
	'''推荐	'''
	def recommend(self,user):
		rank={}
		K=self.sim_movie
		N=self.rec_movie
		#v=similar user 
		user_watched_movie=self.train[user]
		#找到和用户u兴趣最相似的K个用户v
		for v ,wuv in sorted(self.w[user].items(),key=itemgetter(1),reverse=True)[:K]:
			for j in self.train[v]:
				if j in user_watched_movie:
					continue
				rank.setdefault(j,0)
				rank[j]+=wuv
		return sorted(rank.items(),key=itemgetter(1),reverse=True)[:N]
		
if __name__=='__main__':
	user=raw_input()
	usercf=UserBasedCF()
	usercf.SplitData()
	usercf.UserSimilarity()
	for i , x in usercf.recommend(user):
		print i
		
		
