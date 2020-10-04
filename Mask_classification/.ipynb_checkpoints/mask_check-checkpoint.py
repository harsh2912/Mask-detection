from fastai.vision import *
defaults.device = 'cpu'


class maskModel:
    def __init__(self,device):
        defaults.device = device
        self.device = device
        self.learn = load_learner(path='./model',file='model_clean_data.pkl')
        self.learn.model.eval();
        #self.model.model = self.model.model.cpu()
        
    def check_mask(self,faces):
        tensor = torch.from_numpy(faces.astype(np.float32)).permute(0,3,1,2).to(torch.device(self.device))
        tensor = self.learn.data.train_dl.tfms[0]((tensor,torch.ones(len(tensor))))[0]
        print(tensor.max())
        with torch.no_grad():
            out = self.learn.pred_batch(DatasetType.Test,batch=(tensor,torch.ones(len(tensor))))
        #print(out[1].item())
        return ['mask' if i == 0 else 'no_mask' for i in out.argmax(1)]