__author__ = 'amir'


from .St_Strip import St_Strip

L = 20

class Staccato():
    def __init__(self):
        self.calls=0

    def rank(self, M_matrix, e_vector,  strip):
        M = len(M_matrix[0])
        ochiai_vector = strip.calc_ochiai_ranks(M_matrix, e_vector)
        ranks =[]
        for i in range(M):
            if (ochiai_vector[i] > 0):
                ranks.append((i, ochiai_vector[i]))
        sorted_by_second = sorted(ranks, key=lambda tup: tup[1], reverse=True)
        result = []
        for comp,rank in sorted_by_second:
            result.append(comp)
        return result

    def is_in_all_conflicts(self, M_matrix, e_vector,  comp,  strip):
        #get unstripped true conflicts
        conflicts = strip.get_conflic_list(e_vector)
        #process
        #rule out stripped components
        if (strip.is_comp_stripped(comp)):
            return False
        #scan all true conflicts
        for x in conflicts:
            if (M_matrix[x][comp] != 1 ):
                return False
        return True

    def join(self, diagnosis, comp):
        return sorted(list(diagnosis) + [comp])

    def add_if_not_subsumed(self, diagnoses, candidate):
        for current_d in diagnoses:
            if current_d.issubset(candidate):
                return
        diagnoses.append(candidate)

    def runStrip(self, M_matrix, e_vector, strip):
        self.calls += 1
        if (self.calls > L):
            return []
        diagnoses = []
        ranking = self.rank(M_matrix, e_vector, strip)
        unstripped_comps = strip.unstripped_comps_array_Func()
        if (unstripped_comps != []):
            for comp in unstripped_comps:
                if (self.is_in_all_conflicts(M_matrix, e_vector, comp, strip)):
                    diagnoses.append({comp})
                    strip.strip_comp(comp)
        i = 0
        while(i < len(ranking)):
            j = ranking[i]
            if (strip.is_comp_stripped(j)):
                i=i+1
                continue
            if (self.calls <= L):
                temp_strip = strip.clone()
                temp_strip.strip(M_matrix, e_vector, j)
                diagnoses_tag = self.runStrip(M_matrix, e_vector, temp_strip)
            else:
                break
            for tag_diag in diagnoses_tag:
                tag_diag.add(j)
                self.add_if_not_subsumed(diagnoses, tag_diag)
            i=i+1
        return diagnoses

    def run(self, M_matrix,  e_vector):
        #for debug
        self.calls = 0
        N = len(M_matrix)
        M = len(M_matrix[0])
        strip = St_Strip(M, N)
        result = self.runStrip(M_matrix, e_vector, strip)
        return result
