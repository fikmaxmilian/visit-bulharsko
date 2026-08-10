
const sharp=require('sharp');
const fs=require('fs');
const path=require('path');
const base=process.cwd();
const data=JSON.parse(fs.readFileSync(path.join(base,'src/data/site-data.json'),'utf8'));
const dims=JSON.parse(fs.readFileSync(path.join(base,'src/data/image-dimensions.json'),'utf8'));
const posts=data.posts.filter(p=>p.noindex!==true);
const postsByDate=posts.map((post,index)=>({post,index})).sort((a,b)=>{
  const d=new Date(b.post.date||0).getTime()-new Date(a.post.date||0).getTime();
  return d || a.index-b.index;
}).map(x=>x.post);
const byCat=(slug)=>postsByDate.filter(p=>p.categories?.some(c=>c.slug===slug));
const isQuickNews=(post)=>post.postFormat==='quick-news'||post.noImage===true||post.categories?.some(c=>c.slug==='zpravy-bulharsko');
const hero=postsByDate.filter(post=>!isQuickNews(post)).slice(0,4);
const destinations=byCat('nejoblibenejsi-destinace').slice(0,3);
const history=byCat('historie-bulharska').slice(0,2);
const culture=byCat('kultura-a-tradice').slice(0,2);
const needed=[...hero,...destinations,...history,...culture].map(p=>p.featured_image).filter(Boolean);
fs.rmSync(path.join(base,'public/generated/responsive'), {recursive:true, force:true});
const out={};
const widths=[320,480,640,768,960,1200];
(async()=>{
  for (const publicPath of Array.from(new Set(needed))) {
    const meta=dims[publicPath];
    if (!meta) continue;
    const src=path.join(base,'public',publicPath);
    if (!fs.existsSync(src)) continue;
    const originalWidth=meta.width || 0;
    if (originalWidth < 360) continue;
    const ext=path.extname(publicPath);
    const stem=publicPath.slice(1, -ext.length).replace(/[\\/]+/g,'__').replace(/[^a-zA-Z0-9_.-]/g,'-');
    const variants=[];
    for (const w of widths) {
      if (w > originalWidth) continue;
      const outRel=`/generated/responsive/${stem}-${w}.webp`;
      const outFile=path.join(base,'public',outRel);
      fs.mkdirSync(path.dirname(outFile), {recursive:true});
      await sharp(src).resize({width:w, withoutEnlargement:true}).webp({quality:72, effort:4}).toFile(outFile);
      variants.push({src:outRel,width:w});
    }
    if (variants.length) {
      const fallback=variants.find(v=>v.width>=640) || variants[variants.length-1];
      out[publicPath]={src:fallback.src, srcset:variants.map(v=>`${v.src} ${v.width}w`).join(', ')};
    }
  }
  fs.writeFileSync(path.join(base,'src/data/image-responsive.json'), JSON.stringify(out,null,2)+'\n');
  console.log('homepage responsive images', Object.keys(out).length);
})();
