from sklearn.decomposition import TruncatedSVD


class DecompositionFactory:

    @staticmethod
    def get(decomposer: str, number_components):
        if decomposer == 'TruncatedSVD':
            return TruncatedSVD(n_components=number_components)

        return None
