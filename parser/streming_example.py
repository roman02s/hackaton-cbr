from haystack.nodes.prompt import PromptNode

pn = PromptNode("gpt-3.5-turbo", api_key="<api_key_goes_here>", model_kwargs={"stream":True})
prompt = "What are the three most interesting things about Berlin? Be elaborate and use numbered list"
pn(prompt)
# CUSTOM
# from haystack.nodes.prompt import PromptNode
# from haystack.nodes.prompt.invocation_layer.handlers import TokenStreamingHandler
#
#
# class MyCustomTokenStreamingHandler(TokenStreamingHandler):
#
#     def __call__(self, token_received, **kwargs) -> str:
#         # here is your custom logic for each token
#         return token_received
#
#
# custom_handler = MyCustomTokenStreamingHandler()
# pn = PromptNode("gpt-3.5-turbo", api_key="<api_key_goes_here>", model_kwargs={"stream_handler": custom_handler})
# prompt = "What are the three most interesting things about Berlin? Be elaborate and use a numbered list."
# pn(prompt)