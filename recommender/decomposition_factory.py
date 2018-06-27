from sklearn.decomposition import TruncatedSVD, NMF, LatentDirichletAllocation


class DecompositionFactory:

    @staticmethod
    def get(decomposer: str, number_components):
        if decomposer == 'TruncatedSVD':
            return TruncatedSVD(n_components=number_components)

        if decomposer == 'NMF':
            return NMF(n_components=number_components)

        if decomposer == 'LatentDirichletAllocation':
            return LatentDirichletAllocation(n_components=number_components)

        return None
