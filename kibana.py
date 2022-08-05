import json
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Default Dashboar Constant
DEFAULT_DASHBOARD = {'title': 'Snaffler INDEX_NAME Dashboard', 
        'hits': 0,
        'description': 'Automatically generated Snaffler Analysis Dashboard for INDEX_NAME', 
        'panelsJSON': '[{"version":"8.1.1","type":"lens","gridData":{"x":0,"y":0,"w":24,"h":15,"i":"c3fa6c9e-4672-4faa-a9c1-fcaafda4f187"},"panelIndex":"c3fa6c9e-4672-4faa-a9c1-fcaafda4f187","embeddableConfig":{"attributes":{"title":"","visualizationType":"lnsPie","type":"lens","references":[{"type":"index-pattern","id":"DATA-VIEW-ID","name":"indexpattern-datasource-current-indexpattern"},{"type":"index-pattern","id":"DATA-VIEW-ID","name":"indexpattern-datasource-layer-29d70054-bf67-4e38-8e90-86428b2daa8b"}],"state":{"visualization":{"shape":"donut","layers":[{"layerId":"29d70054-bf67-4e38-8e90-86428b2daa8b","groups":["88ff5f6a-1a94-428e-b235-97bef2c9a976"],"metric":"56f31052-f87a-48a5-b5c3-8470faa993b3","numberDisplay":"percent","categoryDisplay":"default","legendDisplay":"default","nestedLegend":false,"layerType":"data"}]},"query":{"query":"","language":"kuery"},"filters":[],"datasourceStates":{"indexpattern":{"layers":{"29d70054-bf67-4e38-8e90-86428b2daa8b":{"columns":{"88ff5f6a-1a94-428e-b235-97bef2c9a976":{"label":"Top values of FileResult.MatchedRule.Triage.keyword","dataType":"string","operationType":"terms","scale":"ordinal","sourceField":"FileResult.MatchedRule.Triage.keyword","isBucketed":true,"params":{"size":5,"orderBy":{"type":"column","columnId":"56f31052-f87a-48a5-b5c3-8470faa993b3"},"orderDirection":"desc","otherBucket":true,"missingBucket":false,"parentFormat":{"id":"terms"}}},"56f31052-f87a-48a5-b5c3-8470faa993b3":{"label":"Count of records","dataType":"number","operationType":"count","isBucketed":false,"scale":"ratio","sourceField":"___records___"}},"columnOrder":["88ff5f6a-1a94-428e-b235-97bef2c9a976","56f31052-f87a-48a5-b5c3-8470faa993b3"],"incompleteColumns":{}}}}}}},"hidePanelTitles":false,"enhancements":{}},"title":"Top Triage Levels Chart"},{"version":"8.1.1","type":"lens","gridData":{"x":24,"y":0,"w":24,"h":15,"i":"8224e538-2801-448b-ab15-851398803236"},"panelIndex":"8224e538-2801-448b-ab15-851398803236","embeddableConfig":{"attributes":{"title":"","visualizationType":"lnsDatatable","type":"lens","references":[{"type":"index-pattern","id":"DATA-VIEW-ID","name":"indexpattern-datasource-current-indexpattern"},{"type":"index-pattern","id":"DATA-VIEW-ID","name":"indexpattern-datasource-layer-26463e1a-6276-4ca7-9cef-c6edf409b99b"}],"state":{"visualization":{"layerId":"26463e1a-6276-4ca7-9cef-c6edf409b99b","layerType":"data","columns":[{"isTransposed":false,"columnId":"de574d0b-cd17-4508-88fc-653c7bf3128a"},{"isTransposed":false,"columnId":"76965224-d6f5-47af-9970-1f9506c03250"}]},"query":{"query":"","language":"kuery"},"filters":[],"datasourceStates":{"indexpattern":{"layers":{"26463e1a-6276-4ca7-9cef-c6edf409b99b":{"columns":{"de574d0b-cd17-4508-88fc-653c7bf3128a":{"label":"Top values of FileResult.MatchedRule.RuleName.keyword","dataType":"string","operationType":"terms","scale":"ordinal","sourceField":"FileResult.MatchedRule.RuleName.keyword","isBucketed":true,"params":{"size":5,"orderBy":{"type":"column","columnId":"76965224-d6f5-47af-9970-1f9506c03250"},"orderDirection":"desc","otherBucket":true,"missingBucket":false,"parentFormat":{"id":"terms"}}},"76965224-d6f5-47af-9970-1f9506c03250":{"label":"Count of records","dataType":"number","operationType":"count","isBucketed":false,"scale":"ratio","sourceField":"___records___"}},"columnOrder":["de574d0b-cd17-4508-88fc-653c7bf3128a","76965224-d6f5-47af-9970-1f9506c03250"],"incompleteColumns":{}}}}}}},"hidePanelTitles":false,"enhancements":{}},"title":"Top Results by Rule Name"},{"version":"8.1.1","type":"lens","gridData":{"x":0,"y":15,"w":24,"h":15,"i":"2bfb56ae-3e97-4dee-b616-98f6b74275c2"},"panelIndex":"2bfb56ae-3e97-4dee-b616-98f6b74275c2","embeddableConfig":{"attributes":{"title":"","visualizationType":"lnsDatatable","type":"lens","references":[{"type":"index-pattern","id":"DATA-VIEW-ID","name":"indexpattern-datasource-current-indexpattern"},{"type":"index-pattern","id":"DATA-VIEW-ID","name":"indexpattern-datasource-layer-6e5e8002-9028-412f-ad49-a130594ed69d"}],"state":{"visualization":{"layerId":"6e5e8002-9028-412f-ad49-a130594ed69d","layerType":"data","columns":[{"isTransposed":false,"columnId":"8761cada-db96-49bb-ad6d-c12dda113e31","width":292.8333333333333},{"isTransposed":false,"columnId":"d4427089-0a99-413e-b408-3f9bf8a0d89b"},{"isTransposed":false,"columnId":"a6102726-a2a4-420c-a04f-9a742ad1b0f1"}]},"query":{"query":"","language":"kuery"},"filters":[],"datasourceStates":{"indexpattern":{"layers":{"6e5e8002-9028-412f-ad49-a130594ed69d":{"columns":{"8761cada-db96-49bb-ad6d-c12dda113e31":{"label":"Top values of FileResult.FileInfo.Name.keyword","dataType":"string","operationType":"terms","scale":"ordinal","sourceField":"FileResult.FileInfo.Name.keyword","isBucketed":true,"params":{"size":3,"orderBy":{"type":"column","columnId":"a6102726-a2a4-420c-a04f-9a742ad1b0f1"},"orderDirection":"desc","otherBucket":true,"missingBucket":false,"parentFormat":{"id":"terms"}}},"d4427089-0a99-413e-b408-3f9bf8a0d89b":{"label":"Top values of FileResult.MatchedRule.RuleName.keyword","dataType":"string","operationType":"terms","scale":"ordinal","sourceField":"FileResult.MatchedRule.RuleName.keyword","isBucketed":true,"params":{"size":3,"orderBy":{"type":"column","columnId":"a6102726-a2a4-420c-a04f-9a742ad1b0f1"},"orderDirection":"desc","otherBucket":true,"missingBucket":false,"parentFormat":{"id":"terms"}}},"a6102726-a2a4-420c-a04f-9a742ad1b0f1":{"label":"Count of records","dataType":"number","operationType":"count","isBucketed":false,"scale":"ratio","sourceField":"___records___"}},"columnOrder":["8761cada-db96-49bb-ad6d-c12dda113e31","d4427089-0a99-413e-b408-3f9bf8a0d89b","a6102726-a2a4-420c-a04f-9a742ad1b0f1"],"incompleteColumns":{}}}}}}},"hidePanelTitles":false,"enhancements":{}},"title":"Top Results by FileName and Matched Rule"},{"version":"8.1.1","type":"lens","gridData":{"x":24,"y":15,"w":24,"h":15,"i":"5bd2f484-7a96-4975-9950-83f7084c3820"},"panelIndex":"5bd2f484-7a96-4975-9950-83f7084c3820","embeddableConfig":{"attributes":{"title":"","visualizationType":"lnsXY","type":"lens","references":[{"type":"index-pattern","id":"DATA-VIEW-ID","name":"indexpattern-datasource-current-indexpattern"},{"type":"index-pattern","id":"DATA-VIEW-ID","name":"indexpattern-datasource-layer-74bd93a9-674a-480a-a6ba-013cec7f5ed5"}],"state":{"visualization":{"legend":{"isVisible":true,"position":"right"},"valueLabels":"hide","fittingFunction":"None","yLeftExtent":{"mode":"full"},"yRightExtent":{"mode":"full"},"axisTitlesVisibilitySettings":{"x":true,"yLeft":true,"yRight":true},"tickLabelsVisibilitySettings":{"x":true,"yLeft":true,"yRight":true},"labelsOrientation":{"x":0,"yLeft":0,"yRight":0},"gridlinesVisibilitySettings":{"x":true,"yLeft":true,"yRight":true},"preferredSeriesType":"bar_stacked","layers":[{"layerId":"74bd93a9-674a-480a-a6ba-013cec7f5ed5","accessors":["aef3149e-ad18-4e81-87bd-a9fba2cd2552"],"position":"top","seriesType":"bar_stacked","showGridlines":false,"layerType":"data","xAccessor":"c6ebfe14-0736-4bf5-aa69-a9d12875da61"}]},"query":{"query":"","language":"kuery"},"filters":[],"datasourceStates":{"indexpattern":{"layers":{"74bd93a9-674a-480a-a6ba-013cec7f5ed5":{"columns":{"c6ebfe14-0736-4bf5-aa69-a9d12875da61":{"label":"Top values of FileResult.FileInfo.Attributes.keyword","dataType":"string","operationType":"terms","scale":"ordinal","sourceField":"FileResult.FileInfo.Attributes.keyword","isBucketed":true,"params":{"size":5,"orderBy":{"type":"column","columnId":"aef3149e-ad18-4e81-87bd-a9fba2cd2552"},"orderDirection":"desc","otherBucket":true,"missingBucket":false,"parentFormat":{"id":"terms"}}},"aef3149e-ad18-4e81-87bd-a9fba2cd2552":{"label":"Count of records","dataType":"number","operationType":"count","isBucketed":false,"scale":"ratio","sourceField":"___records___"}},"columnOrder":["c6ebfe14-0736-4bf5-aa69-a9d12875da61","aef3149e-ad18-4e81-87bd-a9fba2cd2552"],"incompleteColumns":{}}}}}}},"hidePanelTitles":false,"enhancements":{}},"title":"Matched Attributes"},{"version":"8.1.1","type":"lens","gridData":{"x":0,"y":30,"w":24,"h":15,"i":"0b5c7fd5-8502-4779-bf16-6c5db26b25ee"},"panelIndex":"0b5c7fd5-8502-4779-bf16-6c5db26b25ee","embeddableConfig":{"attributes":{"title":"","visualizationType":"lnsDatatable","type":"lens","references":[{"type":"index-pattern","id":"DATA-VIEW-ID","name":"indexpattern-datasource-current-indexpattern"},{"type":"index-pattern","id":"DATA-VIEW-ID","name":"indexpattern-datasource-layer-a77bef1d-15e8-4971-9575-4ec693ce12b9"}],"state":{"visualization":{"layerId":"a77bef1d-15e8-4971-9575-4ec693ce12b9","layerType":"data","columns":[{"isTransposed":false,"columnId":"25be9d9a-0300-41c8-bec9-f5cff36eb429"},{"isTransposed":false,"columnId":"9b569c9f-6ff6-451c-9c20-bf1c28bc596c"}]},"query":{"query":"","language":"kuery"},"filters":[],"datasourceStates":{"indexpattern":{"layers":{"a77bef1d-15e8-4971-9575-4ec693ce12b9":{"columns":{"25be9d9a-0300-41c8-bec9-f5cff36eb429":{"label":"Top values of FileResult.FileInfo.FullName.keyword","dataType":"string","operationType":"terms","scale":"ordinal","sourceField":"FileResult.FileInfo.FullName.keyword","isBucketed":true,"params":{"size":3,"orderBy":{"type":"column","columnId":"9b569c9f-6ff6-451c-9c20-bf1c28bc596c"},"orderDirection":"desc","otherBucket":true,"missingBucket":false,"parentFormat":{"id":"terms"}}},"9b569c9f-6ff6-451c-9c20-bf1c28bc596c":{"label":"Count of records","dataType":"number","operationType":"count","isBucketed":false,"scale":"ratio","sourceField":"___records___"}},"columnOrder":["25be9d9a-0300-41c8-bec9-f5cff36eb429","9b569c9f-6ff6-451c-9c20-bf1c28bc596c"],"incompleteColumns":{}}}}}}},"hidePanelTitles":false,"enhancements":{}},"title":"File Full Name"},{"version":"8.1.1","type":"lens","gridData":{"x":24,"y":30,"w":24,"h":15,"i":"33bd967f-4708-4481-9607-0f8677a8ee7a"},"panelIndex":"33bd967f-4708-4481-9607-0f8677a8ee7a","embeddableConfig":{"attributes":{"title":"","visualizationType":"lnsXY","type":"lens","references":[{"type":"index-pattern","id":"DATA-VIEW-ID","name":"indexpattern-datasource-current-indexpattern"},{"type":"index-pattern","id":"DATA-VIEW-ID","name":"indexpattern-datasource-layer-699466b4-a42e-42d5-81f7-8c841b0b15a3"}],"state":{"visualization":{"legend":{"isVisible":true,"position":"right"},"valueLabels":"hide","fittingFunction":"None","yLeftExtent":{"mode":"full"},"yRightExtent":{"mode":"full"},"axisTitlesVisibilitySettings":{"x":true,"yLeft":true,"yRight":true},"tickLabelsVisibilitySettings":{"x":true,"yLeft":true,"yRight":true},"labelsOrientation":{"x":0,"yLeft":0,"yRight":0},"gridlinesVisibilitySettings":{"x":true,"yLeft":true,"yRight":true},"preferredSeriesType":"bar_stacked","layers":[{"layerId":"699466b4-a42e-42d5-81f7-8c841b0b15a3","accessors":["75f530d5-6589-4447-bd26-0840a3d081ce"],"position":"top","seriesType":"bar_stacked","showGridlines":false,"layerType":"data","xAccessor":"9df227fb-4eae-4cdc-9e22-cf950c914885"}]},"query":{"query":"","language":"kuery"},"filters":[],"datasourceStates":{"indexpattern":{"layers":{"699466b4-a42e-42d5-81f7-8c841b0b15a3":{"columns":{"9df227fb-4eae-4cdc-9e22-cf950c914885":{"label":"Top values of FileResult.TextResult.MatchedStrings.keyword","dataType":"string","operationType":"terms","scale":"ordinal","sourceField":"FileResult.TextResult.MatchedStrings.keyword","isBucketed":true,"params":{"size":5,"orderBy":{"type":"column","columnId":"75f530d5-6589-4447-bd26-0840a3d081ce"},"orderDirection":"desc","otherBucket":true,"missingBucket":false,"parentFormat":{"id":"terms"}}},"75f530d5-6589-4447-bd26-0840a3d081ce":{"label":"Count of records","dataType":"number","operationType":"count","isBucketed":false,"scale":"ratio","sourceField":"___records___"}},"columnOrder":["9df227fb-4eae-4cdc-9e22-cf950c914885","75f530d5-6589-4447-bd26-0840a3d081ce"],"incompleteColumns":{}}}}}}},"hidePanelTitles":false,"enhancements":{}},"title":"Matched Strings"},{"version":"8.1.1","type":"lens","gridData":{"x":0,"y":45,"w":48,"h":11,"i":"aecf7b68-3b3c-4109-8be8-0e98911689a5"},"panelIndex":"aecf7b68-3b3c-4109-8be8-0e98911689a5","embeddableConfig":{"attributes":{"title":"","visualizationType":"lnsDatatable","type":"lens","references":[{"type":"index-pattern","id":"DATA-VIEW-ID","name":"indexpattern-datasource-current-indexpattern"},{"type":"index-pattern","id":"DATA-VIEW-ID","name":"indexpattern-datasource-layer-cc0b500f-41a9-4c40-995f-38dd30318ff2"}],"state":{"visualization":{"layerId":"cc0b500f-41a9-4c40-995f-38dd30318ff2","layerType":"data","columns":[{"columnId":"68dabb3c-6b1e-4f8c-a1ce-a8c2f04adc98"},{"columnId":"cf40b0e4-8a51-46bc-b698-295635ce7497"}]},"query":{"query":"","language":"kuery"},"filters":[],"datasourceStates":{"indexpattern":{"layers":{"cc0b500f-41a9-4c40-995f-38dd30318ff2":{"columns":{"68dabb3c-6b1e-4f8c-a1ce-a8c2f04adc98":{"label":"Top values of FileResult.TextResult.MatchContext.keyword","dataType":"string","operationType":"terms","scale":"ordinal","sourceField":"FileResult.TextResult.MatchContext.keyword","isBucketed":true,"params":{"size":5,"orderBy":{"type":"column","columnId":"cf40b0e4-8a51-46bc-b698-295635ce7497"},"orderDirection":"desc","otherBucket":true,"missingBucket":false,"parentFormat":{"id":"terms"}}},"cf40b0e4-8a51-46bc-b698-295635ce7497":{"label":"Count of records","dataType":"number","operationType":"count","isBucketed":false,"scale":"ratio","sourceField":"___records___"}},"columnOrder":["68dabb3c-6b1e-4f8c-a1ce-a8c2f04adc98","cf40b0e4-8a51-46bc-b698-295635ce7497"],"incompleteColumns":{}}}}}}},"hidePanelTitles":false,"enhancements":{}},"title":"Match Context"}]',
        'optionsJSON': '{"useMargins":true,"syncColors":false,"hidePanelTitles":false}', 
        'version': 1, 
        'timeRestore': False, 
        'kibanaSavedObjectMeta': {
            'searchSourceJSON': '{"query":{"query":"","language":"kuery"},"filter":[]}'
            }
        }

class Kibana:
    _hostname = ""
    _port = ""
    # Does do TLS verification by default. Toggle to true to turn off TLS checking (Used for self signed certificates).
    # Again cause this will translate to verify when we actually run requests we invert it.
    # Does use HTTPS by default. Toggle to true to use HTTP instead of HTTPS.
    _http = False
    _session = None

    def __init__(self, apikey, hostname, port=5601, insecure=False, http=False):
        self._hostname = hostname
        self._port = port
        # setup a session object and then use that for our requests so we don't have to repeat ourselves all the time.
        self._session = requests.Session()
        # inverting here to make sense later.
        self._session.verify = not insecure
        #print(self._session.verify)
        self._session.headers.update({"Authorization": f"ApiKey {apikey}", "kbn-xsrf": "true"})
        # HTTP option is provided since I only test locally and the default with the docker
        # compose is to use HTTP for kibana.
        self._http = http

    # Getters, just in case we need them.
    @property
    def hostname(self):
        return self._hostname

    @property
    def port(self):
        return self._port

    @property
    def http(self):
        return self._http

    @property
    def session(self):
        return self._session

    @property
    def url(self):
        result = ""
        if self._http:
            result = f"http://{self._hostname}:{self._port}"
        else:
            result = f"https://{self._hostname}:{self._port}"
        return result

    @property
    def request_headers(self):
        headers = {"Authorization": f"ApiKey {self.apikey}"}
        return headers

    # Setters too just as well you know.

    @hostname.setter
    def hostname(self, hostname):
        self._hostname = hostname

    @port.setter
    def port(self, port):
        self._port = port

    @session.setter
    def session(self, session):
        self._session = session

    @http.setter
    def http(self, http):
        self._http = http

    def get_saved_object(self, type):
        """
        get_saved_objects: Returns a list of all saved objects within Kibana as a JSON object.
        @imports:
        - type: A string representing the saved object type that we want retrieve.
        Supported types are: ["visualization", "dashboard", "search", "index-pattern", "config"]
        @returns saved_objects: All saved objects that exists within Kibana.
        TODO: Add functionality for supporting padinated results.
        """
        saved_object_types = [
            "visualization",
            "dashboard",
            "search",
            "index-pattern",
            "config"
            ]
        if type not in saved_object_types:
            raise ValueError(f"Provided saved_object_type was {type} but one of {saved_object_types} was expected.")
        r = self.session.get(f"{self.url}/api/saved_objects/_find?type={type}")
        return r.json()['saved_objects']

    def create_data_view(self, pattern, name=None):
        """
        create_data_view: Creates a new index pattern/data view in Kibana using the API.
        This is necessary to create things such as dashboards later on.
        @imports:
        - pattern: The pattern to use for the data-view. This can be used to refer to multiple indices.
        - name: A name to use for the data_view's ID field. This field is optional.
        #- default: Set to False by default, this is used to toggle whether the pattern should be made the
        #default pattern in Kibana.
        """
        exists = False
        r = self.session.get(f"{self.url}/api/saved_objects/_find?type=index-pattern")
        data_views = r.json()["saved_objects"]
        for data_view in data_views: 
            if data_view["attributes"]["title"] == pattern:
                print("Data view already exists!")
                exists = True
        if not exists:
            data = {
                "override": False,
                "refresh_fields": True,
                "data_view": {
                    "title": pattern,
                    "timeFieldName": "DateTime",
                }
            }
            if name is not None:
                data["data_view"]["id"] = name
            r = self.session.post(f"{self.url}/api/data_views/data_view", data=json.dumps(data))

    def create_dashboard(self, new_dashboard):
        """
        create_dashboard: Creates a new dashboard.
        @imports: 
        - new_dashboard: A dictionary representing the new dashboard to be uploaded.
        """
        exists = False
        r = self.session.get(f"{self.url}/api/saved_objects/_find?type=dashboard")
        dashboards = r.json()["saved_objects"]
        for dashboard in dashboards:
            if dashboard["attributes"]["title"] == new_dashboard["title"]:
                print("Dashboard already exists!")
                exists = True
        if not exists:
            data = {
                "attributes": new_dashboard
            }
            r = self.session.post(f"{self.url}/api/saved_objects/dashboard", data=json.dumps(data))
