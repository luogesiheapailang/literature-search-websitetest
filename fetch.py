import requests
from xml.etree import ElementTree as ET


def fetch_pubmed_data(pmids):
    # 构建查询URL
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        'db': 'pubmed',
        'id': ','.join(pmids),  # 多个文献ID，逗号分隔
        'retmode': 'xml',  # 返回 XML 格式
        'retmax': '10'  # 返回的文献数量
    }

    # 发送请求
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        # 解析 XML 响应
        root = ET.fromstring(response.content)
        records = root.findall('.//PubmedArticle')

        # 存储文献数据
        results = []
        for record in records:
            # 提取各字段信息
            title = record.find('.//ArticleTitle').text if record.find('.//ArticleTitle') is not None else ''
            authors = ', '.join([author.find('LastName').text + ' ' + author.find('ForeName').text for author in
                                 record.findall('.//Author')]) if record.findall('.//Author') else ''
            abstract = record.find('.//AbstractText').text if record.find('.//AbstractText') is not None else ''
            publication_year = record.find('.//PubDate/Year').text if record.find('.//PubDate/Year') is not None else ''
            keywords = ', '.join([keyword.text for keyword in record.findall('.//Keyword')]) if record.findall(
                './/Keyword') else ''
            citation_count = record.find('.//CitationCount').text if record.find('.//CitationCount') is not None else ''
            document_id = record.find('.//PMID').text if record.find('.//PMID') is not None else ''

            # 存储数据
            RSoE_data = {
                'AU': authors,
                'TI': title,
                'AB': abstract,
                'PY': publication_year,
                'SC': keywords,
                'NR': citation_count,
                'UT': document_id
            }
            results.append(RSoE_data)

        return results
    else:
        return None


# 示例 PMIDs (PubMed 文献ID)
pmids = ['34398734', '34013275', '33843353']
results = fetch_pubmed_data(pmids)

# 打印获取的文献数据
if results:
    for result in results:
        print(result)
else:
    print("未能获取数据")
