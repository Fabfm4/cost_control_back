from fastapi import HTTPException


def raise_404_error(model_name: str, extra_message: str = ''):
    raise HTTPException(
        status_code=404, detail=f'{model_name} not found {extra_message}')
