import os, json
from typing import List, Optional

from api.models.type import Model

class ModelService:
    def __init__(self):
        with open(os.path.join(os.getcwd(), "public/models.json"), 'r') as f:
            models_data = json.load(f)
        self.models = [Model(**model_data) for model_data in models_data]

    def get_model(self, model_id: str) -> Optional[Model]:
        for model in self.models:
            if model.id == model_id:
                return model
        return None

    def get_model_id(self, model_id: str) -> Optional[str]:
        model = self.get_model(model_id)
        if model is not None:
            return model.id
        return None

    def get_model_name(self, model_id: str) -> Optional[str]:
        model = self.get_model(model_id)
        if model is not None:
            return model.name
        return None

    def get_model_description(self, model_id: str) -> Optional[str]:
        model = self.get_model(model_id)
        if model is not None:
            return model.description
        return None

    def get_model_developer(self, model_id: str) -> Optional[str]:
        model = self.get_model(model_id)
        if model is not None:
            return model.developer
        return None

    def get_model_provider(self, model_id: str) -> Optional[str]:
        model = self.get_model(model_id)
        if model is not None:
            return model.provider
        return None

    def get_model_source(self, model_id: str) -> Optional[str]:
        model = self.get_model(model_id)
        if model is not None:
            return model.source
        return None

    def get_model_tags(self, model_id: str) -> Optional[List[str]]:
        model = self.get_model(model_id)
        if model is not None:
            return model.tags
        return None

    def get_model_max_file_size(self, model_id: str) -> Optional[int]:
        model = self.get_model(model_id)
        if model is not None:
            return model.maxFileSize
        return None

    def get_model_max_context_window(self, model_id: str) -> Optional[int]:
        model = self.get_model(model_id)
        if model is not None:
            return model.maxContextWindow
        return None

    def get_model_pricing(self, model_id: str) -> Optional[float]:
        model = self.get_model(model_id)
        if model is not None:
            return model.pricing
        return None

    def get_model_inference(self, model_id: str) -> Optional[str]:
        model = self.get_model(model_id)
        if model is not None:
            return model.inference
        return None

    def get_active_models(self) -> List[Model]:
        return [model for model in self.models if model.active]

    def get_inactive_models(self) -> List[Model]:
        return [model for model in self.models if not model.active]

    def get_model_ids(self) -> List[str]:
        return [model.id for model in self.models]

    def get_model_names(self) -> List[str]:
        return [model.name for model in self.models]
