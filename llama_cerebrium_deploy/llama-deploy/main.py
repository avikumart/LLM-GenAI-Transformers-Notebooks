import os
from huggingface_hub import login
from pydantic import BaseModel
from vllm import LLM, SamplingParams

# hf login token
login(token=os.environ.get("HF_AUTH_TOKEN"))

# initialize the model
llm = LLM(
    model="meta-llama/Llama-3.2-1B",
    dtype="float16",
    device="cuda",
    gpu_memory_utilization=0.7
)

# set pydantic model
class LLMRequest(BaseModel):
    prompt: str
    max_tokens: int = 256
    temperature: float = 0.8
    top_p: float = 0.95
    top_k: int = 50
    repetition_penalty: float = 1.2


def predict(request: LLMRequest):
    # set sampling params
    sampling_params = SamplingParams(
        max_tokens=request.max_tokens,
        temperature=request.temperature,
        top_p=request.top_p,
        top_k=request.top_k,
        repetition_penalty=request.repetition_penalty
    )

    # generate response
    response = llm.generate(request.prompt, sampling_params=sampling_params)
    return response[0].text
