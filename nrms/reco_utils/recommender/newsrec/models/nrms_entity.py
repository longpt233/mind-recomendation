import torch.nn.functional as F

__all__ = ["NRMSModelEntity"]

from reco_utils.recommender.newsrec.models.nrms import NRMSModel


class NRMSModelEntity(NRMSModel):

    def __init__(self, hparams):
        super().__init__(hparams)

    def news_encoder(self, sequences_input):

        title, entity = sequences_input[:, :self.hparams.title_size], sequences_input[:, self.hparams.title_size:]
        
        y = F.dropout(self.embedding_layer(title), p=self.hparams.dropout).transpose(0, 1)

        q = F.dropout(self.embedding_layer(entity), p=self.hparams.dropout).transpose(0, 1)
        y = self.news_self_att(q, y, y)[0].transpose(0, 1)   # lấy mỗi cái 0 là láy mỗi cái len 
        y = F.dropout(y, p=self.hparams.dropout)
        y = self.news_att_layer(y)
        return y


