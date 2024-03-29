#!/usr/bin/env python
# -*- coding: utf-8 -*-

fileName = raw_input()
with  open(fileName, 'r') as inputFile:

  verbPredictions = []
  nounPredictions = []
  adjPredictions  = []
  currentPredictions = []
  sourceWord = ''

  conjToEnding = {'1C':'are', '2C':'ere', '3C':'ire'}

  def getVerbPrediction(verbPredictions):
    if len(verbPredictions) == 0:
      return None
  
    minLen  = min([len(p[0]) for p in verbPredictions])
    shortestStems = [(p[0], p[3]) for p in verbPredictions if len(p[0]) == minLen]
    areShortestStems = [(stem, conj) for (stem, conj) in shortestStems if conj == '1C']

    stem, conj = areShortestStems[0] if len(areShortestStems) != 0 else shortestStems[0]
    return stem + conjToEnding.setdefault(conj, 'are') + '+V'


  def getNounPrediction(nounPredictions):
    if len(nounPredictions) == 0:
      return None

    minLen  = min([len(p[0]) for p in nounPredictions])
    x = [p for p in nounPredictions if len(p[0]) == minLen][0]
    return x[0] + '+N'



  for line in inputFile:
    if line == '\n':


      # Predictinf vp and modifying if necessary
      vp = getVerbPrediction(verbPredictions)
      if sourceWord[-2:] in ['rò', 'rà']:       vp = sourceWord[:-2] + 're+V'
      if sourceWord[-2:] in ['an', 'ar']:       vp = sourceWord[:-2] + 'are+V'
      if sourceWord[-3:] in ['ata', 'ati']:     vp = sourceWord[:-3] + 'are+V'
      if sourceWord[-3:] in ['ran', 'rai']:     vp = sourceWord[:-3] + 're+V'
      if sourceWord[-4:] in ['rono']:           vp = sourceWord[:-4] + 're+V'
      if sourceWord[-4:] in ['ebbe']:           vp = sourceWord[:-4] + 'e+V'
      if sourceWord[-4:] in ['avan', 'ando']:   vp = sourceWord[:-4] + 'are+V'
      if sourceWord[-5:] in ['ranno', 'remmo', 'ssimo', 'reste', 'resti']: vp = sourceWord[:-5] + 're+V'
      if sourceWord[-5:] in ['avamo', 'avano', 'asser']: vp = sourceWord[:-5] + 'are+V'
      if sourceWord[-5:] == 'ebber':            vp = sourceWord[:-5] + 'e+V'
      if sourceWord[-7:] in ['rebbero']: vp = sourceWord[:-7] + 're+V'
    
      if vp != None and sourceWord[-3:] == 'oni' and vp[-5:] == 'onare': vp = None
    
      # Predicting Noun
      np = getNounPrediction(nounPredictions)
      if sourceWord[-3:] in ['ate']:  np = None
      if sourceWord[-6:] in ['assero']: np = None

      # Predicting Adjective
      ap = None
      if np == None and vp == None and ap == None: ap = sourceWord[:-1] + 'o+A'


      if sourceWord[-4:] == 'assi':
        vp = sourceWord[-4:] + 'are+V'
        np = None
        ap = None


      if np != None and sourceWord[-4:] == 'rono' and np[-6:] == 'rono+N':
        vp = np[:-6] + 're+V'
        np = None
      if np != None and sourceWord[-2:] == 're' and np[-4:] == 'ra+N':
        vp = np[:-4] + 're+V'
        np = None


      if sourceWord[-4:] in ['anti', 'ante']:
        ap = sourceWord[-4:] + 'are+A'
        vp = None
      if ap != None and ap[-5:] == 'roo+A':
        vp = ap[:-5] + 're+V'
        ap = None

      if vp != None: np = None

      answer = sourceWord
      for w in [vp, np, ap]:
        if w != None:
          answer += '\t' + w

      print answer

      verbPredictions = []
      adjPredictions  = []
      nounPredictions = []
  
    else:
      sourceWord, stemWithModifiers = line.split()
      stemWithModifiers = stemWithModifiers.split('+')
      type = stemWithModifiers[1]
      
      if type == 'V': verbPredictions.append(stemWithModifiers)
      if type == 'N': nounPredictions.append(stemWithModifiers)
      if type == 'A': adjPredictions.append(stemWithModifiers)
