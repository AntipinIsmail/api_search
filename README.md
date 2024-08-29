 Сlass Items  - get() - получения элементов таблты есть возможность фильтрации по возрастани и убиванию параметров 
              - post() 

 Class Item - get(id) получения самого элемента
              patch(id)
              del( id)
              
api.add_resource(Items, '/api/items/')/ все элементы если без фильтрации есть фильтры api/items?name=var
&price=-1000(- для отметк начало с какой цены)
&type=var1
&colour=var2
&sort=price,-name,create_date(- для убивания)
api.add_resource(Item, '/api/items/<int:id>') / получения элемента по id
